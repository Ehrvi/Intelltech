"""
System Monitor - Observer Pattern Implementation

Event-driven monitoring with pluggable observers for logging, alerting, metrics.

Pattern: Observer (Gang of Four, 1994)
Purpose: Decouple event generation from event handling
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging
import weakref

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of system events"""
    BOOTSTRAP_START = "bootstrap_start"
    BOOTSTRAP_SUCCESS = "bootstrap_success"
    BOOTSTRAP_FAILURE = "bootstrap_failure"
    ENFORCEMENT_VIOLATION = "enforcement_violation"
    ENFORCEMENT_PASS = "enforcement_pass"
    TASK_START = "task_start"
    TASK_COMPLETE = "task_complete"
    TASK_FAILURE = "task_failure"
    SYSTEM_ERROR = "system_error"


class EventSeverity(Enum):
    """Event severity levels"""
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


@dataclass
class SystemEvent:
    """System event data"""
    type: EventType
    severity: EventSeverity
    message: str
    context: Dict[str, Any]
    timestamp: datetime
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class SystemObserver(ABC):
    """
    Observer Interface - all observers implement this.
    
    Observers react to system events (logging, alerting, metrics, etc.)
    """
    
    @abstractmethod
    def update(self, event: SystemEvent):
        """
        Called when an event occurs.
        
        Args:
            event: The system event that occurred
        """
        pass


class LogObserver(SystemObserver):
    """Observer that logs events"""
    
    def __init__(self, log_level: int = logging.INFO):
        self.log_level = log_level
        self.logger = logging.getLogger("MOTHER.events")
    
    def update(self, event: SystemEvent):
        """Log the event"""
        log_message = f"[{event.type.value}] {event.message}"
        
        if event.severity == EventSeverity.CRITICAL:
            self.logger.critical(log_message, extra=event.context)
        elif event.severity == EventSeverity.ERROR:
            self.logger.error(log_message, extra=event.context)
        elif event.severity == EventSeverity.WARNING:
            self.logger.warning(log_message, extra=event.context)
        elif event.severity == EventSeverity.INFO:
            self.logger.info(log_message, extra=event.context)
        else:
            self.logger.debug(log_message, extra=event.context)


class AlertObserver(SystemObserver):
    """Observer that sends alerts for critical events"""
    
    def __init__(self, severity_threshold: EventSeverity = EventSeverity.ERROR):
        self.threshold = severity_threshold
        self.alert_count = 0
    
    def update(self, event: SystemEvent):
        """Send alert if event is severe enough"""
        if event.severity.value >= self.threshold.value:
            self._send_alert(event)
    
    def _send_alert(self, event: SystemEvent):
        """Send alert (placeholder - would integrate with real alerting system)"""
        self.alert_count += 1
        logger.warning(f"🚨 ALERT #{self.alert_count}: {event.message}")
        # In production: Send to Slack, PagerDuty, email, etc.


class MetricsObserver(SystemObserver):
    """Observer that collects metrics"""
    
    def __init__(self):
        self.metrics = {
            "events_total": 0,
            "events_by_type": {},
            "events_by_severity": {},
            "bootstrap_success_count": 0,
            "bootstrap_failure_count": 0,
            "enforcement_violations": 0,
        }
    
    def update(self, event: SystemEvent):
        """Update metrics"""
        self.metrics["events_total"] += 1
        
        # Count by type
        event_type = event.type.value
        self.metrics["events_by_type"][event_type] = \
            self.metrics["events_by_type"].get(event_type, 0) + 1
        
        # Count by severity
        severity = event.severity.name
        self.metrics["events_by_severity"][severity] = \
            self.metrics["events_by_severity"].get(severity, 0) + 1
        
        # Specific metrics
        if event.type == EventType.BOOTSTRAP_SUCCESS:
            self.metrics["bootstrap_success_count"] += 1
        elif event.type == EventType.BOOTSTRAP_FAILURE:
            self.metrics["bootstrap_failure_count"] += 1
        elif event.type == EventType.ENFORCEMENT_VIOLATION:
            self.metrics["enforcement_violations"] += 1
    
    def get_bootstrap_success_rate(self) -> float:
        """Calculate bootstrap success rate"""
        total = (self.metrics["bootstrap_success_count"] + 
                self.metrics["bootstrap_failure_count"])
        if total == 0:
            return 0.0
        return self.metrics["bootstrap_success_count"] / total
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return {
            **self.metrics,
            "bootstrap_success_rate": self.get_bootstrap_success_rate()
        }


class FileObserver(SystemObserver):
    """Observer that writes events to a file"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.event_count = 0
    
    def update(self, event: SystemEvent):
        """Write event to file"""
        with open(self.filepath, 'a') as f:
            f.write(f"{event.timestamp.isoformat()} | "
                   f"{event.severity.name} | "
                   f"{event.type.value} | "
                   f"{event.message}\n")
        self.event_count += 1


class SystemMonitor:
    """
    Subject in Observer Pattern.
    
    Maintains list of observers and notifies them of events.
    Uses WeakSet to prevent memory leaks from forgotten observers.
    """
    
    def __init__(self):
        # Use WeakSet for automatic cleanup of dead observers
        self._observers = weakref.WeakSet()
        self.event_count = 0
        logger.info("SystemMonitor initialized")
    
    def attach(self, observer: SystemObserver):
        """
        Attach an observer.
        
        Args:
            observer: Observer to attach
        """
        self._observers.add(observer)
        logger.debug(f"Attached observer: {observer.__class__.__name__}")
    
    def detach(self, observer: SystemObserver):
        """
        Detach an observer.
        
        Args:
            observer: Observer to detach
        """
        self._observers.discard(observer)
        logger.debug(f"Detached observer: {observer.__class__.__name__}")
    
    def notify(self, event: SystemEvent):
        """
        Notify all observers of an event.
        
        Args:
            event: Event to notify observers about
        """
        self.event_count += 1
        
        # Notify all observers
        # Use list() to avoid "Set changed size during iteration" error
        for observer in list(self._observers):
            try:
                observer.update(event)
            except Exception as e:
                # Don't let one observer's failure break others
                logger.error(f"Observer {observer.__class__.__name__} failed: {e}")
    
    # Convenience methods for common events
    
    def on_bootstrap_start(self):
        """Notify bootstrap started"""
        self.notify(SystemEvent(
            type=EventType.BOOTSTRAP_START,
            severity=EventSeverity.INFO,
            message="Bootstrap initialization started",
            context={},
            timestamp=datetime.now()
        ))
    
    def on_bootstrap_success(self, duration_seconds: float):
        """Notify bootstrap succeeded"""
        self.notify(SystemEvent(
            type=EventType.BOOTSTRAP_SUCCESS,
            severity=EventSeverity.INFO,
            message=f"Bootstrap completed successfully in {duration_seconds:.2f}s",
            context={"duration": duration_seconds},
            timestamp=datetime.now()
        ))
    
    def on_bootstrap_failure(self, error: Exception):
        """Notify bootstrap failed"""
        self.notify(SystemEvent(
            type=EventType.BOOTSTRAP_FAILURE,
            severity=EventSeverity.CRITICAL,
            message=f"Bootstrap failed: {str(error)}",
            context={"error": str(error), "error_type": type(error).__name__},
            timestamp=datetime.now()
        ))
    
    def on_enforcement_violation(self, principle: str, message: str):
        """Notify enforcement violation"""
        self.notify(SystemEvent(
            type=EventType.ENFORCEMENT_VIOLATION,
            severity=EventSeverity.ERROR,
            message=f"{principle} violated: {message}",
            context={"principle": principle},
            timestamp=datetime.now()
        ))
    
    def on_enforcement_pass(self, principle: str):
        """Notify enforcement passed"""
        self.notify(SystemEvent(
            type=EventType.ENFORCEMENT_PASS,
            severity=EventSeverity.DEBUG,
            message=f"{principle} compliance verified",
            context={"principle": principle},
            timestamp=datetime.now()
        ))


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create monitor
    monitor = SystemMonitor()
    
    # Attach observers
    log_observer = LogObserver()
    alert_observer = AlertObserver(severity_threshold=EventSeverity.ERROR)
    metrics_observer = MetricsObserver()
    
    monitor.attach(log_observer)
    monitor.attach(alert_observer)
    monitor.attach(metrics_observer)
    
    # Simulate events
    monitor.on_bootstrap_start()
    monitor.on_enforcement_pass("P1")
    monitor.on_enforcement_violation("P2", "Asked user to decide")
    monitor.on_bootstrap_success(duration_seconds=3.5)
    
    # Check metrics
    print("\n=== Metrics Summary ===")
    metrics = metrics_observer.get_metrics_summary()
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    print(f"\nTotal events processed: {monitor.event_count}")
    print(f"Alerts sent: {alert_observer.alert_count}")
