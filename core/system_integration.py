import logging
import threading
import time
from dataclasses import dataclass, field
from fnmatch import fnmatchcase
from queue import Queue, Full, Empty
from threading import RLock, Thread, Event
from time import monotonic
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


Callback = Callable[[str, Dict[str, Any]], None]


ALLOWED_EVENTS: Set[str] = frozenset(
    {
        "system_initialized",
        "system_shutdown",
        "cost_gate_blocked",
        "cost_saved",
        "knowledge_reused",
        "knowledge_created",
        "quality_validated",
        "quality_failed",
        "task_routed",
    }
)


@dataclass(order=True)
class _DelayedItem:
    """Item container for delayed scheduling in a heap."""
    due_time: float
    seq: int
    task: "DeliveryTask" = field(compare=False)


@dataclass
class Subscription:
    """Represents a subscription from a system to a pattern with a callback."""
    system_name: str
    pattern: str
    callback: Callback
    order: int  # Increasing order to pick latest registration


@dataclass
class DeliveryTask:
    """Represents a delivery attempt of a single event to a single subscriber."""
    event: str
    data: Dict[str, Any]
    system_name: str
    callback: Callback
    attempt: int = 0
    max_attempts: int = 3
    next_attempt_time: float = field(default_factory=monotonic)


class SystemBus:
    """
    System Integration Bus for Manus Global Knowledge System.

    An in-memory, thread-safe, event-driven message bus that supports:
    - Publish-subscribe with pattern-based routing (fnmatch, e.g., 'cost.*')
    - Direct messaging to specific recipients
    - Broadcast to all matched subscribers
    - Event queue with at-least-once delivery guarantees and retries
    - Health monitoring via get_health()

    Notes:
    - Event names for send/broadcast must be part of the supported set.
    - Subscribers may register pattern-based subscriptions; during delivery,
      a system receives each event at most once (zero overlaps), even if
      multiple patterns within that system match an event.
    """

    def __init__(
        self,
        max_queue_size: int = 10000,
        max_retries: int = 3,
        backoff_base: float = 0.2,
        backoff_factor: float = 2.0,
        enqueue_timeout: float = 2.0,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Initialize the SystemBus.

        Args:
            max_queue_size: Maximum number of delivery tasks allowed in the immediate queue.
            max_retries: Maximum retry attempts per delivery task on failure.
            backoff_base: Initial backoff in seconds for retry scheduling.
            backoff_factor: Multiplicative factor for exponential backoff.
            enqueue_timeout: Seconds to wait when the queue is full before dropping a task.
            logger: Optional pre-configured logger; if None, a default logger is created.

        Raises:
            ValueError: If provided parameters are invalid.
        """
        if max_queue_size <= 0:
            raise ValueError("max_queue_size must be > 0")
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        if backoff_base <= 0.0:
            raise ValueError("backoff_base must be > 0")
        if backoff_factor < 1.0:
            raise ValueError("backoff_factor must be >= 1.0")
        if enqueue_timeout < 0.0:
            raise ValueError("enqueue_timeout must be >= 0")

        self._logger = logger or self._default_logger()

        self._lock = RLock()
        self._order_counter = 0

        # Subscriptions: global ordered list (registration order)
        self._subscriptions: List[Subscription] = []

        # Per-system map for quick unsubscribe by exact pattern string
        self._subscriptions_by_system: Dict[str, Dict[str, Subscription]] = {}

        # Immediate delivery queue
        self._queue: Queue[DeliveryTask] = Queue(maxsize=max_queue_size)

        # Delayed (scheduled) tasks heap
        self._delayed_heap: List[_DelayedItem] = []
        self._delayed_seq = 0  # tie-breaker for heap items

        # Worker thread controls
        self._stop_event: Event = Event()
        self._worker: Thread = Thread(target=self._run, name="SystemBusWorker", daemon=True)

        # Delivery configuration
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._backoff_factor = backoff_factor
        self._enqueue_timeout = enqueue_timeout

        # Health metrics
        self._start_time = time.time()
        self._metrics: Dict[str, Any] = {
            "enqueued": 0,
            "delivered": 0,
            "failed": 0,
            "retries": 0,
            "dropped": 0,
            "last_error": None,
            "last_event_time": None,
        }

        self._worker.start()
        self._logger.debug("SystemBus initialized and worker thread started.")

    def subscribe(self, event: str, callback: Callback, system_name: str) -> None:
        """
        Subscribe a system to an event pattern.

        The event parameter supports fnmatch-style patterns, e.g., 'cost_*', 'quality.*'.
        When a matching event is delivered, the provided callback is invoked with:
        callback(event_name, data_dict)

        If the same system subscribes multiple times with overlapping patterns that
        match a given event, the system will still receive that event only once.
        The most recently registered matching subscription's callback is used.

        Args:
            event: Event name pattern (fnmatch-style).
            callback: Callable that handles the event: (event_name, data).
            system_name: Unique identifier for the subscribing system.

        Raises:
            ValueError: If parameters are invalid.
        """
        if not isinstance(event, str) or not event:
            raise ValueError("event must be a non-empty string pattern")
        if not callable(callback):
            raise ValueError("callback must be callable")
        if not isinstance(system_name, str) or not system_name:
            raise ValueError("system_name must be a non-empty string")

        with self._lock:
            self._order_counter += 1
            sub = Subscription(system_name=system_name, pattern=event, callback=callback, order=self._order_counter)

            by_pattern = self._subscriptions_by_system.setdefault(system_name, {})
            # Replace existing same-pattern subscription for that system if present
            existing = by_pattern.get(event)
            if existing:
                try:
                    # Remove the old one from global ordered list
                    self._subscriptions.remove(existing)
                except ValueError:
                    pass  # In case it was already removed
            by_pattern[event] = sub
            self._subscriptions.append(sub)
            self._logger.info("System '%s' subscribed to pattern '%s'.", system_name, event)

    def unsubscribe(self, event: str, system_name: str) -> None:
        """
        Unsubscribe a system from a specific event pattern.

        Args:
            event: The exact event pattern previously subscribed with.
            system_name: The system identifier.

        Raises:
            ValueError: If parameters are invalid.
        """
        if not isinstance(event, str) or not event:
            raise ValueError("event must be a non-empty string pattern")
        if not isinstance(system_name, str) or not system_name:
            raise ValueError("system_name must be a non-empty string")

        with self._lock:
            by_pattern = self._subscriptions_by_system.get(system_name)
            if not by_pattern:
                self._logger.warning(
                    "Unsubscribe requested for unknown system '%s' (pattern '%s').", system_name, event
                )
                return

            sub = by_pattern.pop(event, None)
            if sub:
                try:
                    self._subscriptions.remove(sub)
                except ValueError:
                    pass
                self._logger.info("System '%s' unsubscribed from pattern '%s'.", system_name, event)
            else:
                self._logger.warning(
                    "Unsubscribe requested for system '%s' but no such pattern '%s' was registered.",
                    system_name,
                    event,
                )

            if not by_pattern:
                # Clean up empty system map
                self._subscriptions_by_system.pop(system_name, None)

    def send(self, event: str, data: Dict[str, Any], recipients: List[str]) -> None:
        """
        Send an event directly to the specified recipient systems.

        Only systems that have at least one subscription pattern that matches
        the provided event will receive the message. Each system will receive
        the event at most once.

        Args:
            event: The event name (must be one of the supported events).
            data: The event payload dictionary.
            recipients: List of target system names.

        Raises:
            ValueError: If parameters are invalid or event is not supported.
        """
        self._validate_event_name(event)
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")
        if not isinstance(recipients, list) or not all(isinstance(x, str) and x for x in recipients):
            raise ValueError("recipients must be a list of non-empty strings")
        if not recipients:
            self._logger.warning("send called with empty recipients; nothing will be enqueued.")
            return

        recipients_set = set(recipients)
        tasks = self._build_delivery_tasks(event, data, recipients=recipients_set)
        self._enqueue_tasks(tasks)

        # Warn for requested recipients that are not subscribed to this event
        targeted_systems = {t.system_name for t in tasks}
        unreachable = recipients_set - targeted_systems
        if unreachable:
            self._logger.warning(
                "send to event '%s': some recipients have no matching subscription: %s",
                event,
                sorted(unreachable),
            )

    def broadcast(self, event: str, data: Dict[str, Any]) -> None:
        """
        Broadcast an event to all systems with matching subscriptions.

        Args:
            event: The event name (must be one of the supported events).
            data: The event payload dictionary.

        Raises:
            ValueError: If parameters are invalid or event is not supported.
        """
        self._validate_event_name(event)
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")

        tasks = self._build_delivery_tasks(event, data, recipients=None)
        self._enqueue_tasks(tasks)

    def get_health(self) -> Dict[str, Any]:
        """
        Retrieve health and telemetry information for the bus.

        Returns:
            A dictionary containing:
            - start_time: Wall-clock time when the bus started.
            - uptime_seconds
            - enqueued: Total tasks enqueued (including retries).
            - delivered: Successfully delivered tasks.
            - failed: Tasks that exhausted retries.
            - retries: Number of retry attempts performed.
            - dropped: Tasks dropped due to full queue.
            - subscribers_count: Number of active subscriptions (pattern-level).
            - systems_count: Number of systems with at least one subscription.
            - queue_size: Number of immediate tasks pending.
            - delayed_size: Number of delayed (scheduled) tasks.
            - worker_alive: Whether the worker thread is alive.
            - last_error: Last error message observed (if any).
            - last_event_time: Monotonic timestamp of last enqueue or delivery operation.
        """
        with self._lock:
            now = time.time()
            health = {
                "start_time": self._start_time,
                "uptime_seconds": max(0.0, now - self._start_time),
                "enqueued": self._metrics["enqueued"],
                "delivered": self._metrics["delivered"],
                "failed": self._metrics["failed"],
                "retries": self._metrics["retries"],
                "dropped": self._metrics["dropped"],
                "subscribers_count": len(self._subscriptions),
                "systems_count": len(self._subscriptions_by_system),
                "queue_size": self._queue.qsize(),
                "delayed_size": len(self._delayed_heap),
                "worker_alive": self._worker.is_alive(),
                "last_error": self._metrics["last_error"],
                "last_event_time": self._metrics["last_event_time"],
            }
        return health

    # ---------------- Internal helpers ----------------

    def _validate_event_name(self, event: str) -> None:
        if not isinstance(event, str) or not event:
            raise ValueError("event must be a non-empty string")
        if event not in ALLOWED_EVENTS:
            raise ValueError(f"Unsupported event '{event}'. Supported events: {sorted(ALLOWED_EVENTS)}")

    def _build_delivery_tasks(
        self,
        event: str,
        data: Dict[str, Any],
        recipients: Optional[Set[str]] = None,
    ) -> List[DeliveryTask]:
        """
        Build de-duplicated delivery tasks for the given event and optional recipient filter.

        Args:
            event: Event name to match against subscriptions.
            data: Event payload.
            recipients: Optional set of system names to target; if None, broadcast to all.

        Returns:
            List of DeliveryTask instances.
        """
        with self._lock:
            # Iterate in reverse registration order so most recent subscription wins for a system
            selected_callbacks: Dict[str, Callback] = {}

            for sub in reversed(self._subscriptions):
                if recipients is not None and sub.system_name not in recipients:
                    continue
                if sub.system_name in selected_callbacks:
                    continue
                if fnmatchcase(event, sub.pattern):
                    selected_callbacks[sub.system_name] = sub.callback

            tasks: List[DeliveryTask] = []
            now = monotonic()
            for system, cb in selected_callbacks.items():
                # Shallow copy to isolate per-recipient mutations
                payload = dict(data)
                tasks.append(
                    DeliveryTask(
                        event=event,
                        data=payload,
                        system_name=system,
                        callback=cb,
                        attempt=0,
                        max_attempts=self._max_retries,
                        next_attempt_time=now,
                    )
                )

            return tasks

    def _enqueue_tasks(self, tasks: List[DeliveryTask]) -> None:
        if not tasks:
            self._logger.debug("No matching subscriptions; nothing enqueued.")
            return

        enqueued = 0
        dropped = 0
        last_event_time = monotonic()

        for task in tasks:
            try:
                self._queue.put(task, timeout=self._enqueue_timeout)
                enqueued += 1
            except Full:
                self._logger.error(
                    "Immediate queue is full; dropping task for system '%s', event '%s'.",
                    task.system_name,
                    task.event,
                )
                dropped += 1

        with self._lock:
            self._metrics["enqueued"] += enqueued
            self._metrics["dropped"] += dropped
            self._metrics["last_event_time"] = last_event_time

        if enqueued:
            self._logger.debug("Enqueued %d task(s).", enqueued)

    def _run(self) -> None:
        """Worker thread loop to process immediate and delayed delivery tasks."""
        try:
            while not self._stop_event.is_set():
                # Deliver due delayed tasks
                self._drain_delayed_ready()

                # Try to get new immediate tasks
                try:
                    task = self._queue.get(timeout=0.1)
                except Empty:
                    # No immediate tasks; consider sleeping until next delayed due
                    self._sleep_until_next_due()
                    continue

                # If task has a scheduled delay, schedule it instead of delivering now
                now = monotonic()
                if task.next_attempt_time > now:
                    self._schedule_delayed(task)
                    continue

                self._deliver(task)
                self._queue.task_done()
        except Exception as exc:
            # Unexpected worker exception; log and continue loop to keep liveness.
            self._logger.exception("Worker encountered unhandled exception: %s", exc)
            with self._lock:
                self._metrics["last_error"] = str(exc)
            # Sleep briefly to avoid tight crash loops
            time.sleep(0.5)

    def _deliver(self, task: DeliveryTask) -> None:
        """Attempt to deliver task, handle success/failure with retries."""
        try:
            task.callback(task.event, task.data)
        except Exception as exc:
            self._logger.exception(
                "Error delivering event '%s' to system '%s' (attempt %d/%d): %s",
                task.event,
                task.system_name,
                task.attempt + 1,
                task.max_attempts + 1,
                exc,
            )
            with self._lock:
                self._metrics["retries"] += 1
                self._metrics["last_error"] = str(exc)
                self._metrics["last_event_time"] = monotonic()

            if task.attempt < task.max_attempts:
                task.attempt += 1
                delay = self._backoff_base * (self._backoff_factor ** (task.attempt - 1))
                task.next_attempt_time = monotonic() + delay
                self._schedule_delayed(task)
            else:
                with self._lock:
                    self._metrics["failed"] += 1
        else:
            with self._lock:
                self._metrics["delivered"] += 1
                self._metrics["last_event_time"] = monotonic()

    def _schedule_delayed(self, task: DeliveryTask) -> None:
        """Schedule a task for later delivery using the delayed heap."""
        with self._lock:
            self._delayed_seq += 1
            item = _DelayedItem(due_time=task.next_attempt_time, seq=self._delayed_seq, task=task)
            # Push into heap (implemented as list + insort since heapq isn't imported explicitly)
            # Using heapq would be ideal, but we can simulate by inserting in order.
            # For correctness and efficiency, import heapq.
            import heapq  # Local import to avoid polluting global namespace
            heapq.heappush(self._delayed_heap, item)

    def _drain_delayed_ready(self) -> None:
        """Move due delayed tasks back to the immediate queue or deliver if ready."""
        import heapq

        now = monotonic()
        moved = 0
        with self._lock:
            while self._delayed_heap and self._delayed_heap[0].due_time <= now:
                item = heapq.heappop(self._delayed_heap)
                # Try to put back to immediate queue for uniform processing
                try:
                    self._queue.put_nowait(item.task)
                    moved += 1
                except Full:
                    # If immediate queue is full, re-insert delayed with minimal delay to retry soon
                    item.task.next_attempt_time = monotonic() + 0.05
                    heapq.heappush(self._delayed_heap, _DelayedItem(item.task.next_attempt_time, item.seq, item.task))
                    break  # Avoid busy loop if queue remains full

        if moved:
            self._logger.debug("Moved %d delayed task(s) to immediate queue.", moved)

    def _sleep_until_next_due(self) -> None:
        """Sleep briefly until the next delayed task is due, if any."""
        with self._lock:
            if not self._delayed_heap:
                return
            next_due = self._delayed_heap[0].due_time
        delay = max(0.0, next_due - monotonic())
        if delay > 0:
            time.sleep(min(delay, 0.1))

    def _default_logger(self) -> logging.Logger:
        """Create a default logger if none is supplied."""
        logger = logging.getLogger("SystemBus")
        if not logger.handlers:
            handler = logging.StreamHandler()
            fmt = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
            )
            handler.setFormatter(fmt)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def __del__(self) -> None:
        """Best-effort attempt to stop the worker on garbage collection."""
        try:
            self._stop_event.set()
        except Exception:
            pass
        # Daemon thread will exit with process; we won't join here to avoid blocking in __del__.