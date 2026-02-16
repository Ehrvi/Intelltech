"""
MOTHER V4 - Main Entry Point

Integrates all components: Bootstrap, Enforcement, Monitoring, Knowledge Loading.
"""

import sys
import logging
from pathlib import Path
from typing import Optional

# Add mother_v4 to path
sys.path.insert(0, str(Path(__file__).parent))

from application.services.bootstrap_facade import BootstrapFacade, BootstrapError
from application.services.enforcement_engine import (
    EnforcementEngine,
    TaskContext,
    EnforcementResult
)
from application.services.system_monitor import (
    SystemMonitor,
    LogObserver,
    AlertObserver,
    MetricsObserver
)
from application.services.knowledge_loader import KnowledgeLoader


class MOTHER:
    """
    Main MOTHER V4 class - integrates all subsystems.
    
    This is the single entry point for using MOTHER V4.
    """
    
    def __init__(self, environment: str = "development", base_path: Optional[Path] = None):
        """
        Initialize MOTHER V4.
        
        Args:
            environment: 'production', 'test', or 'development'
            base_path: Base path for knowledge files (auto-detect if None)
        """
        self.environment = environment
        self.base_path = base_path or self._detect_base_path()
        
        # Core components
        self.bootstrap: Optional[BootstrapFacade] = None
        self.enforcement: Optional[EnforcementEngine] = None
        self.monitor: Optional[SystemMonitor] = None
        self.knowledge: Optional[KnowledgeLoader] = None
        
        # State
        self.initialized = False
        
        # Setup logging
        self._setup_logging()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"MOTHER V4 created (environment: {environment})")
    
    def _detect_base_path(self) -> Path:
        """Auto-detect base path"""
        # Assume we're in mother_v4/ directory
        current = Path(__file__).parent
        # Go up to manus_global_knowledge/
        base = current.parent
        return base
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_level = logging.DEBUG if self.environment == "development" else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def initialize(self) -> bool:
        """
        Initialize MOTHER V4 system.
        
        Returns:
            True if initialization successful
        
        Raises:
            BootstrapError: If initialization fails
        """
        if self.initialized:
            self.logger.warning("MOTHER already initialized")
            return True
        
        try:
            self.logger.info("=" * 60)
            self.logger.info("MOTHER V4 Initialization Starting")
            self.logger.info("=" * 60)
            
            # 1. Setup monitoring first (so we can monitor bootstrap)
            self.logger.info("Step 1/4: Setting up monitoring...")
            self._setup_monitoring()
            
            # 2. Bootstrap
            self.logger.info("Step 2/4: Bootstrapping system...")
            self.monitor.on_bootstrap_start()
            
            self.bootstrap = BootstrapFacade(environment=self.environment)
            bootstrap_success = self.bootstrap.initialize()
            
            if not bootstrap_success:
                raise BootstrapError("Bootstrap failed")
            
            self.monitor.on_bootstrap_success(duration_seconds=0.5)  # TODO: Measure actual time
            
            # 3. Setup enforcement
            self.logger.info("Step 3/4: Setting up enforcement...")
            self._setup_enforcement()
            
            # 4. Load knowledge
            self.logger.info("Step 4/4: Loading knowledge base...")
            self._load_knowledge()
            
            self.initialized = True
            
            self.logger.info("=" * 60)
            self.logger.info("✓ MOTHER V4 Initialization Complete")
            self.logger.info("=" * 60)
            
            # Display status
            self._display_status()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            if self.monitor:
                self.monitor.on_bootstrap_failure(e)
            raise
    
    def _setup_monitoring(self):
        """Setup monitoring system"""
        self.monitor = SystemMonitor()
        
        # Attach observers
        self.monitor.attach(LogObserver())
        self.monitor.attach(AlertObserver())
        self.monitor.attach(MetricsObserver())
        
        self.logger.debug("Monitoring system ready")
    
    def _setup_enforcement(self):
        """Setup enforcement engine"""
        self.enforcement = EnforcementEngine()
        self.logger.debug(f"Enforcement engine ready with {len(self.enforcement.strategies)} strategies")
    
    def _load_knowledge(self):
        """Load knowledge base"""
        self.knowledge = KnowledgeLoader(self.base_path)
        self.knowledge.build_knowledge_tree()
        
        success = self.knowledge.load_all()
        
        if not success:
            self.logger.warning("Some knowledge failed to load (non-critical)")
        else:
            self.logger.info("Knowledge base loaded successfully")
    
    def _display_status(self):
        """Display system status"""
        print("\n" + "=" * 60)
        print("MOTHER V4 STATUS")
        print("=" * 60)
        print(f"Environment: {self.environment}")
        print(f"Base Path: {self.base_path}")
        print(f"Initialized: {self.initialized}")
        print(f"Bootstrap: {'✓' if self.bootstrap else '✗'}")
        print(f"Enforcement: {'✓' if self.enforcement else '✗'} ({len(self.enforcement.strategies) if self.enforcement else 0} strategies)")
        print(f"Monitoring: {'✓' if self.monitor else '✗'}")
        print(f"Knowledge: {'✓' if self.knowledge and self.knowledge.loaded else '✗'}")
        
        if self.knowledge:
            stats = self.knowledge.get_statistics()
            print(f"Knowledge Files: {stats.get('total_files', 0)}")
        
        print("=" * 60 + "\n")
    
    def enforce_task(self, context: TaskContext) -> list[EnforcementResult]:
        """
        Enforce principles for a task.
        
        Args:
            context: Task context for enforcement
        
        Returns:
            List of enforcement results
        """
        if not self.initialized:
            raise RuntimeError("MOTHER not initialized. Call initialize() first.")
        
        results = self.enforcement.enforce_all(context)
        
        # Notify monitor
        for result in results:
            if result.passed:
                self.monitor.on_enforcement_pass(result.principle)
            else:
                self.monitor.on_enforcement_violation(result.principle, result.message)
        
        return results
    
    def search_knowledge(self, query: str):
        """
        Search knowledge base.
        
        Args:
            query: Search query
        
        Returns:
            List of matching knowledge components
        """
        if not self.initialized:
            raise RuntimeError("MOTHER not initialized. Call initialize() first.")
        
        return self.knowledge.search(query)
    
    def get_metrics(self) -> dict:
        """Get system metrics"""
        if not self.initialized or not self.monitor:
            return {}
        
        # Find metrics observer
        for observer in self.monitor._observers:
            if isinstance(observer, MetricsObserver):
                return observer.get_metrics_summary()
        
        return {}
    
    def shutdown(self):
        """Shutdown MOTHER system"""
        self.logger.info("Shutting down MOTHER V4...")
        self.initialized = False
        self.logger.info("MOTHER V4 shutdown complete")


def main():
    """Main entry point for MOTHER V4"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MOTHER V4 - Manus Operating System")
    parser.add_argument(
        "--env",
        choices=["production", "test", "development"],
        default="development",
        help="Environment to run in"
    )
    parser.add_argument(
        "--test-enforcement",
        action="store_true",
        help="Run enforcement test"
    )
    
    args = parser.parse_args()
    
    # Create and initialize MOTHER
    mother = MOTHER(environment=args.env)
    mother.initialize()
    
    # Test enforcement if requested
    if args.test_enforcement:
        print("\n" + "=" * 60)
        print("TESTING ENFORCEMENT")
        print("=" * 60)
        
        # Test 1: Research task without research (P1 violation)
        print("\nTest 1: Research task without research (should fail P1)")
        context1 = TaskContext(
            task_type="research",
            task_description="Find papers",
            used_annas_archive=False,
            used_browser=False
        )
        results1 = mother.enforce_task(context1)
        for r in results1:
            status = "✓ PASS" if r.passed else "✗ FAIL"
            print(f"  {status} - {r.principle}: {r.message}")
        
        # Test 2: Compliant research task
        print("\nTest 2: Research task with Anna's Archive (should pass all)")
        context2 = TaskContext(
            task_type="research",
            task_description="Find papers",
            used_annas_archive=True,
            cost_estimate=2.5,
            quality_score=0.9
        )
        results2 = mother.enforce_task(context2)
        for r in results2:
            status = "✓ PASS" if r.passed else "✗ FAIL"
            print(f"  {status} - {r.principle}: {r.message}")
        
        # Display metrics
        print("\n" + "=" * 60)
        print("METRICS")
        print("=" * 60)
        metrics = mother.get_metrics()
        for key, value in metrics.items():
            print(f"{key}: {value}")
    
    # Shutdown
    mother.shutdown()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
