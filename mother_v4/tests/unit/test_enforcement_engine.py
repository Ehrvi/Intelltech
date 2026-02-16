"""
Unit Tests for EnforcementEngine

Tests Strategy pattern implementation for P1-P7 enforcement.
"""

import pytest
import sys
sys.path.insert(0, '/home/ubuntu/manus_global_knowledge/mother_v4')

from application.services.enforcement_engine import (
    EnforcementEngine,
    EnforcementStrategy,
    EnforcementResult,
    TaskContext,
    Severity,
    P1_AlwaysStudyFirst,
    P2_DecideAutonomously,
    P3_OptimizeCost,
    P4_EnsureQuality,
    P7_AlwaysBeTruthful
)


class TestTaskContext:
    """Test TaskContext"""
    
    def test_task_context_creation(self):
        """Test creating valid task context"""
        context = TaskContext(
            task_type="research",
            task_description="Test task"
        )
        assert context.task_type == "research"
        assert context.used_annas_archive == False  # Default
    
    def test_task_context_validates_type(self):
        """Test task context validates task_type"""
        with pytest.raises(AssertionError):
            TaskContext(
                task_type="invalid_type",
                task_description="Test"
            )


class TestP1_AlwaysStudyFirst:
    """Test P1 enforcement strategy"""
    
    def test_p1_passes_for_research_with_annas_archive(self):
        """Test P1 passes when research uses Anna's Archive"""
        strategy = P1_AlwaysStudyFirst()
        context = TaskContext(
            task_type="research",
            task_description="Find papers",
            used_annas_archive=True
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == True
        assert result.principle == "P1"
    
    def test_p1_passes_for_research_with_browser(self):
        """Test P1 passes when research uses browser"""
        strategy = P1_AlwaysStudyFirst()
        context = TaskContext(
            task_type="research",
            task_description="Find papers",
            used_browser=True
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == True
    
    def test_p1_fails_for_research_without_research(self):
        """Test P1 fails when research task has no actual research"""
        strategy = P1_AlwaysStudyFirst()
        context = TaskContext(
            task_type="research",
            task_description="Find papers",
            used_annas_archive=False,
            used_browser=False
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == False
        assert result.severity == Severity.CRITICAL
        assert "MUST use Anna's Archive" in result.message
    
    def test_p1_passes_for_non_research_tasks(self):
        """Test P1 passes for non-research tasks"""
        strategy = P1_AlwaysStudyFirst()
        context = TaskContext(
            task_type="implementation",
            task_description="Write code"
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == True


class TestP2_DecideAutonomously:
    """Test P2 enforcement strategy"""
    
    def test_p2_passes_when_no_user_question(self):
        """Test P2 passes when AI decides autonomously"""
        strategy = P2_DecideAutonomously()
        context = TaskContext(
            task_type="decision",
            task_description="Choose approach",
            asked_user_to_decide=False
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == True
    
    def test_p2_fails_when_asking_user(self):
        """Test P2 fails when asking user to decide"""
        strategy = P2_DecideAutonomously()
        context = TaskContext(
            task_type="decision",
            task_description="Choose approach",
            asked_user_to_decide=True
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == False
        assert result.severity == Severity.ERROR


class TestP3_OptimizeCost:
    """Test P3 enforcement strategy"""
    
    def test_p3_passes_within_budget(self):
        """Test P3 passes when cost is within budget"""
        strategy = P3_OptimizeCost()
        context = TaskContext(
            task_type="research",
            task_description="Task",
            cost_estimate=5.0,
            cost_budget=10.0
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == True
    
    def test_p3_fails_over_budget(self):
        """Test P3 fails when cost exceeds budget"""
        strategy = P3_OptimizeCost()
        context = TaskContext(
            task_type="research",
            task_description="Task",
            cost_estimate=15.0,
            cost_budget=10.0
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == False
        assert result.severity == Severity.WARNING


class TestP4_EnsureQuality:
    """Test P4 enforcement strategy"""
    
    def test_p4_passes_high_quality(self):
        """Test P4 passes for high quality work"""
        strategy = P4_EnsureQuality()
        context = TaskContext(
            task_type="implementation",
            task_description="Task",
            quality_score=0.85
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == True
    
    def test_p4_fails_low_quality(self):
        """Test P4 fails for low quality work"""
        strategy = P4_EnsureQuality()
        context = TaskContext(
            task_type="implementation",
            task_description="Task",
            quality_score=0.5
        )
        
        result = strategy.enforce(context)
        
        assert result.passed == False
        assert result.severity == Severity.ERROR


class TestEnforcementEngine:
    """Test EnforcementEngine (Context)"""
    
    def test_engine_initializes_with_default_strategies(self):
        """Test engine initializes with P1-P7 by default"""
        engine = EnforcementEngine()
        
        assert len(engine.strategies) == 5  # P1, P2, P3, P4, P7
    
    def test_engine_can_add_strategy(self):
        """Test adding strategy at runtime"""
        engine = EnforcementEngine(strategies=[])
        assert len(engine.strategies) == 0
        
        engine.add_strategy(P1_AlwaysStudyFirst())
        assert len(engine.strategies) == 1
    
    def test_engine_can_remove_strategy(self):
        """Test removing strategy"""
        engine = EnforcementEngine()
        initial_count = len(engine.strategies)
        
        engine.remove_strategy("P1: Always Study First")
        assert len(engine.strategies) == initial_count - 1
    
    def test_engine_enforces_all_strategies(self):
        """Test engine runs all strategies"""
        engine = EnforcementEngine()
        context = TaskContext(
            task_type="research",
            task_description="Test",
            used_annas_archive=True,
            cost_estimate=5.0,
            quality_score=0.9
        )
        
        results = engine.enforce_all(context)
        
        assert len(results) == 5  # One result per strategy
        assert all(isinstance(r, EnforcementResult) for r in results)
    
    def test_engine_calculates_compliance_rate(self):
        """Test compliance rate calculation"""
        engine = EnforcementEngine()
        
        # All pass
        context_pass = TaskContext(
            task_type="implementation",
            task_description="Test",
            quality_score=0.9
        )
        results_pass = engine.enforce_all(context_pass)
        assert engine.get_compliance_rate(results_pass) == 1.0
        
        # Some fail
        context_fail = TaskContext(
            task_type="research",
            task_description="Test",
            used_annas_archive=False,  # P1 violation
            quality_score=0.9
        )
        results_fail = engine.enforce_all(context_fail)
        rate = engine.get_compliance_rate(results_fail)
        assert 0.0 < rate < 1.0  # Some passed, some failed
    
    def test_engine_handles_strategy_exceptions(self):
        """Test engine handles exceptions in strategies gracefully"""
        class FailingStrategy(EnforcementStrategy):
            @property
            def principle_name(self):
                return "Failing Strategy"
            
            def enforce(self, context):
                raise ValueError("Test exception")
        
        engine = EnforcementEngine(strategies=[FailingStrategy()])
        context = TaskContext(task_type="other", task_description="Test")
        
        results = engine.enforce_all(context)
        
        assert len(results) == 1
        assert results[0].passed == False
        assert "failed" in results[0].message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
