"""
Enforcement Engine - Strategy Pattern Implementation

Runtime enforcement of P1-P7 principles using pluggable strategies.

Pattern: Strategy (Gang of Four, 1994)
Purpose: Make enforcement extensible, testable, and actually work
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Severity(Enum):
    """Enforcement violation severity"""
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


@dataclass
class EnforcementResult:
    """Result of an enforcement check"""
    principle: str
    passed: bool
    severity: Severity
    message: str
    context: Dict[str, Any]


@dataclass
class TaskContext:
    """Context information for enforcement checks"""
    task_type: str  # 'research', 'implementation', 'decision', etc.
    task_description: str
    used_annas_archive: bool = False
    used_browser: bool = False
    asked_user_to_decide: bool = False
    cost_estimate: float = 0.0
    cost_budget: float = 100.0
    has_tests: bool = False
    quality_score: float = 0.0
    
    def __post_init__(self):
        """Validate context"""
        assert self.task_type in ['research', 'implementation', 'decision', 'query', 'other']


class EnforcementStrategy(ABC):
    """
    Strategy Interface - all enforcement strategies implement this.
    
    Each principle (P1-P7) is a concrete strategy.
    """
    
    @property
    @abstractmethod
    def principle_name(self) -> str:
        """Name of the principle (e.g., 'P1: Always Study First')"""
        pass
    
    @abstractmethod
    def enforce(self, context: TaskContext) -> EnforcementResult:
        """
        Enforce the principle given task context.
        
        Args:
            context: Information about the current task
        
        Returns:
            EnforcementResult: Pass/fail with details
        """
        pass


class P1_AlwaysStudyFirst(EnforcementStrategy):
    """
    P1: Always Study First
    
    Research tasks MUST use Anna's Archive or browser research.
    """
    
    @property
    def principle_name(self) -> str:
        return "P1: Always Study First"
    
    def enforce(self, context: TaskContext) -> EnforcementResult:
        if context.task_type == "research":
            if not (context.used_annas_archive or context.used_browser):
                return EnforcementResult(
                    principle="P1",
                    passed=False,
                    severity=Severity.CRITICAL,
                    message="Research task detected but no actual research performed. "
                            "MUST use Anna's Archive or browser.",
                    context={"task_type": context.task_type}
                )
        
        return EnforcementResult(
            principle="P1",
            passed=True,
            severity=Severity.INFO,
            message="P1 compliance verified",
            context={}
        )


class P2_DecideAutonomously(EnforcementStrategy):
    """
    P2: Always Decide Autonomously
    
    Don't ask user to make decisions that AI should make.
    """
    
    @property
    def principle_name(self) -> str:
        return "P2: Always Decide Autonomously"
    
    def enforce(self, context: TaskContext) -> EnforcementResult:
        if context.asked_user_to_decide:
            return EnforcementResult(
                principle="P2",
                passed=False,
                severity=Severity.ERROR,
                message="Asked user to decide. AI should make autonomous decisions.",
                context={"asked": True}
            )
        
        return EnforcementResult(
            principle="P2",
            passed=True,
            severity=Severity.INFO,
            message="P2 compliance verified",
            context={}
        )


class P3_OptimizeCost(EnforcementStrategy):
    """
    P3: Always Optimize Cost
    
    Use most cost-effective approach, but CORRECTNESS > COST.
    """
    
    @property
    def principle_name(self) -> str:
        return "P3: Always Optimize Cost"
    
    def enforce(self, context: TaskContext) -> EnforcementResult:
        if context.cost_estimate > context.cost_budget:
            return EnforcementResult(
                principle="P3",
                passed=False,
                severity=Severity.WARNING,
                message=f"Cost ${context.cost_estimate:.2f} exceeds budget ${context.cost_budget:.2f}",
                context={"cost": context.cost_estimate, "budget": context.cost_budget}
            )
        
        return EnforcementResult(
            principle="P3",
            passed=True,
            severity=Severity.INFO,
            message=f"Cost ${context.cost_estimate:.2f} within budget",
            context={"cost": context.cost_estimate}
        )


class P4_EnsureQuality(EnforcementStrategy):
    """
    P4: Always Ensure Quality
    
    Quality score must meet threshold.
    """
    
    @property
    def principle_name(self) -> str:
        return "P4: Always Ensure Quality"
    
    def enforce(self, context: TaskContext) -> EnforcementResult:
        QUALITY_THRESHOLD = 0.8
        
        if context.quality_score < QUALITY_THRESHOLD:
            return EnforcementResult(
                principle="P4",
                passed=False,
                severity=Severity.ERROR,
                message=f"Quality score {context.quality_score:.1%} below threshold {QUALITY_THRESHOLD:.1%}",
                context={"score": context.quality_score, "threshold": QUALITY_THRESHOLD}
            )
        
        return EnforcementResult(
            principle="P4",
            passed=True,
            severity=Severity.INFO,
            message=f"Quality score {context.quality_score:.1%} meets threshold",
            context={"score": context.quality_score}
        )


class P7_AlwaysBeTruthful(EnforcementStrategy):
    """
    P7: Always Be Truthful
    
    This is checked manually - placeholder for future automated checks.
    """
    
    @property
    def principle_name(self) -> str:
        return "P7: Always Be Truthful"
    
    def enforce(self, context: TaskContext) -> EnforcementResult:
        # Truthfulness is hard to check automatically
        # This is a placeholder - actual check would analyze output
        return EnforcementResult(
            principle="P7",
            passed=True,
            severity=Severity.INFO,
            message="P7 requires manual verification",
            context={}
        )


class EnforcementEngine:
    """
    Context for Strategy Pattern.
    
    Manages a collection of enforcement strategies and executes them.
    """
    
    def __init__(self, strategies: List[EnforcementStrategy] = None):
        """
        Args:
            strategies: List of enforcement strategies. If None, uses default P1-P7.
        """
        if strategies is None:
            # Default: All principles
            strategies = [
                P1_AlwaysStudyFirst(),
                P2_DecideAutonomously(),
                P3_OptimizeCost(),
                P4_EnsureQuality(),
                P7_AlwaysBeTruthful(),
            ]
        
        self.strategies = strategies
        logger.info(f"EnforcementEngine initialized with {len(strategies)} strategies")
    
    def add_strategy(self, strategy: EnforcementStrategy):
        """Add a new enforcement strategy at runtime"""
        self.strategies.append(strategy)
        logger.info(f"Added strategy: {strategy.principle_name}")
    
    def remove_strategy(self, principle: str):
        """Remove an enforcement strategy"""
        self.strategies = [s for s in self.strategies if s.principle_name != principle]
        logger.info(f"Removed strategy: {principle}")
    
    def enforce_all(self, context: TaskContext) -> List[EnforcementResult]:
        """
        Run all enforcement strategies.
        
        Args:
            context: Task context for enforcement
        
        Returns:
            List of enforcement results (one per strategy)
        """
        results = []
        
        for strategy in self.strategies:
            try:
                result = strategy.enforce(context)
                results.append(result)
                
                if not result.passed:
                    logger.warning(f"{result.principle} VIOLATION: {result.message}")
                    self._handle_violation(result)
                else:
                    logger.debug(f"{result.principle} passed")
                    
            except Exception as e:
                logger.error(f"Strategy {strategy.principle_name} failed: {e}")
                results.append(EnforcementResult(
                    principle=strategy.principle_name,
                    passed=False,
                    severity=Severity.ERROR,
                    message=f"Enforcement check failed: {e}",
                    context={}
                ))
        
        return results
    
    def _handle_violation(self, result: EnforcementResult):
        """Handle enforcement violation"""
        if result.severity == Severity.CRITICAL:
            # Critical violations could block execution
            logger.critical(f"CRITICAL VIOLATION: {result.message}")
            # In production, might raise exception here
        elif result.severity == Severity.ERROR:
            logger.error(f"ERROR: {result.message}")
        elif result.severity == Severity.WARNING:
            logger.warning(f"WARNING: {result.message}")
    
    def get_compliance_rate(self, results: List[EnforcementResult]) -> float:
        """Calculate compliance rate from results"""
        if not results:
            return 0.0
        passed = sum(1 for r in results if r.passed)
        return passed / len(results)


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create enforcement engine
    engine = EnforcementEngine()
    
    # Example 1: Research task without research (P1 violation)
    context = TaskContext(
        task_type="research",
        task_description="Find papers on software architecture",
        used_annas_archive=False,  # Violation!
        used_browser=False
    )
    
    results = engine.enforce_all(context)
    print(f"\nCompliance rate: {engine.get_compliance_rate(results):.1%}")
    
    # Example 2: Compliant task
    context2 = TaskContext(
        task_type="research",
        task_description="Find papers on software architecture",
        used_annas_archive=True,  # Compliant!
        cost_estimate=2.50,
        quality_score=0.85
    )
    
    results2 = engine.enforce_all(context2)
    print(f"\nCompliance rate: {engine.get_compliance_rate(results2):.1%}")
