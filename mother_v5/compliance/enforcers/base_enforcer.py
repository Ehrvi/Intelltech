#!/usr/bin/env python3
"""
MOTHER V5 - Base Enforcer
=========================

Base class for all MOTHER principle enforcers.

Author: MOTHER V5 Compliance System
Version: 1.0.0
Date: 2026-02-16
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from enum import Enum


class Severity(Enum):
    """Violation severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    BLOCKING = "BLOCKING"


class ComplianceResult:
    """Result of a compliance check."""
    
    def __init__(
        self,
        passed: bool,
        principle: str,
        message: str,
        severity: Severity = Severity.INFO,
        context: Dict[str, Any] = None
    ):
        self.passed = passed
        self.principle = principle
        self.message = message
        self.severity = severity
        self.context = context or {}
    
    def __bool__(self):
        """Allow boolean evaluation of result."""
        return self.passed
    
    def __repr__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"<ComplianceResult {status} [{self.principle}] {self.severity.value}: {self.message}>"


class BaseEnforcer(ABC):
    """
    Base class for all MOTHER principle enforcers.
    
    Each enforcer implements the check() method to validate
    compliance with a specific MOTHER principle.
    """
    
    def __init__(self):
        self.principle_id = self.get_principle_id()
        self.principle_name = self.get_principle_name()
        self.target_compliance = self.get_target_compliance()
        self.severity = self.get_severity()
    
    @abstractmethod
    def get_principle_id(self) -> str:
        """Return the principle ID (e.g., 'P1', 'P2')."""
        pass
    
    @abstractmethod
    def get_principle_name(self) -> str:
        """Return the principle name (e.g., 'Always Study First')."""
        pass
    
    @abstractmethod
    def get_target_compliance(self) -> float:
        """Return the target compliance percentage (0.0 to 1.0)."""
        pass
    
    @abstractmethod
    def get_severity(self) -> Severity:
        """Return the severity level for violations."""
        pass
    
    @abstractmethod
    def check(self, context: Dict[str, Any]) -> ComplianceResult:
        """
        Check compliance with this principle.
        
        Args:
            context: Dictionary containing relevant context for the check.
                     The structure depends on the specific enforcer.
        
        Returns:
            ComplianceResult object indicating pass/fail and details.
        """
        pass
    
    def _pass(self, message: str, context: Dict[str, Any] = None) -> ComplianceResult:
        """Helper to create a passing result."""
        return ComplianceResult(
            passed=True,
            principle=self.principle_id,
            message=message,
            severity=Severity.INFO,
            context=context
        )
    
    def _fail(self, message: str, context: Dict[str, Any] = None) -> ComplianceResult:
        """Helper to create a failing result."""
        return ComplianceResult(
            passed=False,
            principle=self.principle_id,
            message=message,
            severity=self.severity,
            context=context
        )
    
    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.principle_id}] target={self.target_compliance*100}%>"


class EnforcerRegistry:
    """
    Registry for all enforcers.
    
    Provides a central place to register and retrieve enforcers.
    """
    
    def __init__(self):
        self._enforcers: Dict[str, BaseEnforcer] = {}
    
    def register(self, enforcer: BaseEnforcer):
        """Register an enforcer."""
        self._enforcers[enforcer.principle_id] = enforcer
    
    def get(self, principle_id: str) -> BaseEnforcer:
        """Get an enforcer by principle ID."""
        return self._enforcers.get(principle_id)
    
    def get_all(self) -> Dict[str, BaseEnforcer]:
        """Get all registered enforcers."""
        return self._enforcers.copy()
    
    def __len__(self):
        return len(self._enforcers)
    
    def __repr__(self):
        return f"<EnforcerRegistry {len(self)} enforcers registered>"


# Global registry instance
ENFORCER_REGISTRY = EnforcerRegistry()
