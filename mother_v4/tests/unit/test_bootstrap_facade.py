"""
Unit Tests for BootstrapFacade

Tests Facade and Template Method patterns implementation.
"""

import pytest
import sys
sys.path.insert(0, '/home/ubuntu/manus_global_knowledge/mother_v4')

from application.services.bootstrap_facade import (
    BootstrapFacade,
    BootstrapError,
    Bootstrapper,
    ProductionBootstrapper,
    TestBootstrapper,
    DevelopmentBootstrapper
)


class MockBootstrapper(Bootstrapper):
    """Mock bootstrapper for testing"""
    
    def __init__(self):
        self.custom_logic_called = False
    
    def run_custom_logic(self):
        self.custom_logic_called = True


class FailingBootstrapper(Bootstrapper):
    """Bootstrapper that fails for testing error handling"""
    
    def run_custom_logic(self):
        raise ValueError("Intentional failure for testing")


class TestBootstrapFacade:
    """Test BootstrapFacade"""
    
    def test_facade_creates_correct_bootstrapper_production(self):
        """Test facade creates ProductionBootstrapper for production env"""
        facade = BootstrapFacade(environment='production')
        assert isinstance(facade.bootstrapper, ProductionBootstrapper)
    
    def test_facade_creates_correct_bootstrapper_test(self):
        """Test facade creates TestBootstrapper for test env"""
        facade = BootstrapFacade(environment='test')
        assert isinstance(facade.bootstrapper, TestBootstrapper)
    
    def test_facade_creates_correct_bootstrapper_development(self):
        """Test facade creates DevelopmentBootstrapper for dev env"""
        facade = BootstrapFacade(environment='development')
        assert isinstance(facade.bootstrapper, DevelopmentBootstrapper)
    
    def test_facade_simple_interface(self):
        """Test facade provides simple interface"""
        facade = BootstrapFacade(environment='test')
        # Should not raise exception
        result = facade.initialize()
        assert result == True


class TestTemplateMethod:
    """Test Template Method pattern in Bootstrapper"""
    
    def test_template_method_calls_all_steps(self):
        """Test template method calls all required steps"""
        bootstrapper = MockBootstrapper()
        
        result = bootstrapper.initialize()
        
        assert result == True
        assert bootstrapper.custom_logic_called == True
    
    def test_template_method_handles_failure(self):
        """Test template method handles failures correctly"""
        bootstrapper = FailingBootstrapper()
        
        with pytest.raises(BootstrapError) as exc_info:
            bootstrapper.initialize()
        
        assert "Intentional failure" in str(exc_info.value)
    
    def test_hook_method_can_be_overridden(self):
        """Test hook methods can be overridden by subclasses"""
        test_bootstrapper = TestBootstrapper()
        
        # TestBootstrapper overrides should_load_principles to return False
        assert test_bootstrapper.should_load_principles() == False
        
        # ProductionBootstrapper uses default (True)
        prod_bootstrapper = ProductionBootstrapper()
        assert prod_bootstrapper.should_load_principles() == True


class TestProductionBootstrapper:
    """Test ProductionBootstrapper"""
    
    def test_production_bootstrapper_initializes(self):
        """Test production bootstrapper can initialize"""
        bootstrapper = ProductionBootstrapper()
        result = bootstrapper.initialize()
        assert result == True


class TestTestBootstrapper:
    """Test TestBootstrapper"""
    
    def test_test_bootstrapper_skips_principles(self):
        """Test test bootstrapper skips principle loading"""
        bootstrapper = TestBootstrapper()
        assert bootstrapper.should_load_principles() == False
    
    def test_test_bootstrapper_initializes(self):
        """Test test bootstrapper can initialize"""
        bootstrapper = TestBootstrapper()
        result = bootstrapper.initialize()
        assert result == True


class TestDevelopmentBootstrapper:
    """Test DevelopmentBootstrapper"""
    
    def test_development_bootstrapper_initializes(self):
        """Test development bootstrapper can initialize"""
        bootstrapper = DevelopmentBootstrapper()
        result = bootstrapper.initialize()
        assert result == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
