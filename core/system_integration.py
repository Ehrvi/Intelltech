#!/usr/bin/env python3
"""
System Integration Bus - Refactored
Improved thread safety, exception handling, and shutdown logic.
"""

import logging
import threading
import time
import heapq
from dataclasses import dataclass, field
from fnmatch import fnmatchcase
from queue import Queue, Full, Empty
from threading import RLock, Thread, Event
from time import monotonic
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

Callback = Callable[[str, Dict[str, Any]], None]

# A set of known event patterns that are expected to be published.
# Subscribing to a pattern not in this set will generate a warning.
KNOWN_EVENT_PATTERNS = frozenset({
    "uep.enforce.start", "uep.level1.blocked", "uep.level2.blocked",
    "uep.level3.reused", "uep.level4.routed", "uep.level4.routed_escalated",
    "uep.level5.validation_failed", "uep.level6.learned", "uep.enforce.end"
})

@dataclass(order=True)
class _DelayedItem:
    due_time: float
    seq: int
    task: "DeliveryTask" = field(compare=False)

@dataclass
class Subscription:
    system_name: str
    pattern: str
    callback: Callback
    order: int

@dataclass
class DeliveryTask:
    event: str
    data: Dict[str, Any]
    system_name: str
    callback: Callback
    attempt: int = 0
    max_attempts: int = 3
    next_attempt_time: float = field(default_factory=monotonic)

class SystemBus:
    """A thread-safe, in-memory event bus with retry and queuing."""

    def __init__(self, max_queue_size: int = 10000, max_retries: int = 3, logger: Optional[logging.Logger] = None):
        self._logger = logger or self._default_logger()
        self._lock = RLock()
        self._order_counter = 0
        self._subscriptions: List[Subscription] = []
        self._queue: Queue[DeliveryTask] = Queue(maxsize=max_queue_size)
        self._delayed_heap: List[_DelayedItem] = []
        self._delayed_seq = 0
        self._stop_event = Event()
        self._worker = Thread(target=self._run, name="SystemBusWorker", daemon=True)
        self._max_retries = max_retries
        self._metrics = {"enqueued": 0, "delivered": 0, "failed": 0, "retries": 0, "dropped": 0}
        self._worker.start()
        self._logger.debug("SystemBus initialized.")

    def subscribe(self, event_pattern: str, callback: Callback, system_name: str) -> None:
        if not any(fnmatchcase(known_pattern, event_pattern) for known_pattern in KNOWN_EVENT_PATTERNS):
            self._logger.warning(f"System '{system_name}' subscribing to a potentially un-published event pattern: '{event_pattern}'")
        with self._lock:
            self._order_counter += 1
            sub = Subscription(system_name, event_pattern, callback, self._order_counter)
            self._subscriptions.append(sub)
            self._logger.info(f"System '{system_name}' subscribed to '{event_pattern}'.")

    def publish(self, event: str, data: Dict[str, Any]) -> None:
        tasks = self._build_delivery_tasks(event, data)
        self._enqueue_tasks(tasks)

    def shutdown(self, timeout: Optional[float] = 5.0) -> None:
        self._logger.info("SystemBus shutting down...")
        self._stop_event.set()
        self._worker.join(timeout)
        if self._worker.is_alive():
            self._logger.warning("Worker thread did not shut down gracefully within the timeout.")

    def _build_delivery_tasks(self, event: str, data: Dict[str, Any]) -> List[DeliveryTask]:
        tasks = []
        delivered_to_systems: Set[str] = set()
        with self._lock:
            # Iterate over a copy to be thread-safe
            subs = list(self._subscriptions)
        
        # Iterate in reverse to prioritize most recent subscriptions
        for sub in reversed(subs):
            if sub.system_name in delivered_to_systems:
                continue
            if fnmatchcase(event, sub.pattern):
                tasks.append(DeliveryTask(event, data, sub.system_name, sub.callback, max_attempts=self._max_retries))
                delivered_to_systems.add(sub.system_name)
        return tasks

    def _enqueue_tasks(self, tasks: List[DeliveryTask]):
        for task in tasks:
            try:
                self._queue.put(task, timeout=2.0)
                self._metrics["enqueued"] += 1
            except Full:
                self._metrics["dropped"] += 1
                self._logger.error(f"Queue is full. Dropping event '{task.event}' for system '{task.system_name}'.")

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                task = self._queue.get(timeout=0.1)
                self._process_task(task)
            except Empty:
                self._move_delayed_to_immediate()
                continue
            except Exception as e:
                self._logger.exception(f"Critical error in SystemBus worker loop: {e}")
                time.sleep(1) # Avoid busy-looping on critical errors

    def _process_task(self, task: DeliveryTask):
        try:
            task.callback(task.event, task.data)
            self._metrics["delivered"] += 1
        except Exception as e:
            self._logger.warning(f"Callback for event '{task.event}' to system '{task.system_name}' failed (attempt {task.attempt + 1}). Error: {e}")
            task.attempt += 1
            if task.attempt < task.max_attempts:
                self._metrics["retries"] += 1
                backoff = 0.2 * (2 ** task.attempt)
                task.next_attempt_time = monotonic() + backoff
                with self._lock:
                    self._delayed_seq += 1
                    heapq.heappush(self._delayed_heap, _DelayedItem(task.next_attempt_time, self._delayed_seq, task))
            else:
                self._metrics["failed"] += 1
                self._logger.error(f"Event '{task.event}' failed delivery to '{task.system_name}' after {task.max_attempts} attempts.")

    def _move_delayed_to_immediate(self):
        now = monotonic()
        with self._lock:
            while self._delayed_heap and self._delayed_heap[0].due_time <= now:
                item = heapq.heappop(self._delayed_heap)
                self._enqueue_tasks([item.task])

    def _default_logger(self) -> logging.Logger:
        logger = logging.getLogger("SystemBus")
        if not logger.handlers:
            handler = logging.StreamHandler()
            fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
            handler.setFormatter(fmt)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
