#!/usr/bin/env python3
"""
Mandatory Initialization Script for Manus Global Knowledge System v2.0

This script MUST be run at the start of every task to:
1. Initialize all system components
2. Load configurations
3. Set up enforcement pipeline
4. Load AI University lessons
5. Verify system health

Usage:
    python3 /home/ubuntu/manus_global_knowledge/mandatory_init.py
"""

import sys
from pathlib import Path

# Add to path
BASE_PATH = Path(__file__).parent
sys.path.insert(0, str(BASE_PATH))

import logging
from typing import Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_configurations() -> Dict[str, Any]:
    """Load all YAML configurations from rules/ directory."""
    import yaml
    
    rules_path = BASE_PATH / "rules"
    configs = {}
    
    config_files = [
        "cost_rules.yaml",
        "quality_rules.yaml",
        "routing_rules.yaml",
        "enforcement_config.yaml",
        "integration_config.yaml",
        "scientific_method_rules.yaml"
    ]
    
    for config_file in config_files:
        config_path = rules_path / config_file
        if config_path.exists():
            with open(config_path, 'r') as f:
                configs[config_file.replace('.yaml', '')] = yaml.safe_load(f)
            logger.info(f"✓ Loaded {config_file}")
        else:
            logger.warning(f"⚠ Missing {config_file}")
    
    return configs


def load_ai_university() -> Dict[str, str]:
    """Load AI University lessons."""
    lessons_path = BASE_PATH / "ai_university" / "lessons"
    lessons = {}
    
    if lessons_path.exists():
        for lesson_file in lessons_path.glob("LESSON_*.md"):
            with open(lesson_file, 'r') as f:
                lessons[lesson_file.stem] = f.read()
        logger.info(f"✓ Loaded {len(lessons)} AI University lessons")
    else:
        logger.warning("⚠ AI University lessons directory not found")
    
    return lessons


def initialize_system_bus():
    """Initialize the System Integration Bus."""
    try:
        from core.system_integration import SystemBus
        bus = SystemBus()
        logger.info("✓ System Bus initialized")
        return bus
    except Exception as e:
        logger.error(f"✗ Failed to initialize System Bus: {e}")
        return None


def initialize_enforcement_pipeline(configs: Dict[str, Any]):
    """Initialize the Unified Enforcement Pipeline."""
    try:
        from core.unified_enforcement import UnifiedEnforcementPipeline
        pipeline = UnifiedEnforcementPipeline(BASE_PATH)
        logger.info("✓ Unified Enforcement Pipeline initialized")
        return pipeline
    except Exception as e:
        logger.error(f"✗ Failed to initialize Enforcement Pipeline: {e}")
        return None


def verify_system_health() -> bool:
    """Verify all systems are operational."""
    checks = {
        "configurations": (BASE_PATH / "rules").exists(),
        "core_modules": (BASE_PATH / "core").exists(),
        "ai_university": (BASE_PATH / "ai_university").exists(),
        "metrics": (BASE_PATH / "metrics").exists(),
        "scientific_enforcement": (BASE_PATH / "core" / "mandatory_scientific_enforcement.py").exists(),
        "cost_reporter": (BASE_PATH / "core" / "auto_cost_reporter.py").exists(),
        "visual_identity_detector": (BASE_PATH / "core" / "visual_identity_detector.py").exists(),
        "design_system_generator": (BASE_PATH / "modules" / "design_system_generator.py").exists(),
    }
    
    all_passed = all(checks.values())
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        logger.info(f"{status} {check}: {'OK' if passed else 'FAILED'}")
    
    return all_passed


def main():
    """Main initialization function."""
    print("=" * 70)
    print("🚀 Manus Global Knowledge System v2.0 - Initialization")
    print("=" * 70)
    print()
    
    # Step 1: Load configurations
    print("📋 Step 1: Loading configurations...")
    configs = load_configurations()
    print()
    
    # Step 2: Load AI University
    print("🎓 Step 2: Loading AI University...")
    lessons = load_ai_university()
    print()
    
    # Step 3: Initialize System Bus
    print("🔌 Step 3: Initializing System Bus...")
    bus = initialize_system_bus()
    print()
    
    # Step 4: Initialize Enforcement Pipeline
    print("🛡️  Step 4: Initializing Enforcement Pipeline...")
    pipeline = initialize_enforcement_pipeline(configs)
    print()
    
    # Step 5: Verify system health
    print("🏥 Step 5: Verifying system health...")
    health_ok = verify_system_health()
    print()
    
    # Summary
    print("=" * 70)
    if health_ok and bus and pipeline:
        print("✅ SYSTEM INITIALIZED SUCCESSFULLY")
        print()
        print("Motto: 'Somente unidos seremos mais fortes!'")
        print()
        print("System ready for:")
        print("  • Total enforcement (6 levels)")
        print("  • Cost optimization (75%+ savings)")
        print("  • Knowledge reuse (prevent duplicates)")
        print("  • Quality assurance (Guardian ≥80%)")
        print("  • Scientific methodology (12 steps)")
        print("  • Bibliographic references (MANDATORY)")
        print("  • Anna's Archive integration (MANDATORY for academic research)")
        print("  • Automatic visual identity detection (Nível 3)")
        print("  • Continuous learning")
        print()
        print("⚠️  MANDATORY ENFORCEMENT ACTIVE:")
        print("  • EVERY output MUST follow MOTHER Operating System V2.0")
        print("  • EVERY scientific claim MUST have bibliographic reference")
        print("  • EVERY conversation MUST end with cost report")
        print("  • Violations = BLOCKING (output will be rejected)")
    else:
        print("⚠️  SYSTEM INITIALIZATION INCOMPLETE")
        print("Please check errors above and fix before proceeding.")
        sys.exit(1)
    
    print("=" * 70)
    
    return {
        'configs': configs,
        'lessons': lessons,
        'bus': bus,
        'pipeline': pipeline,
        'health': health_ok
    }


if __name__ == '__main__':
    result = main()
    sys.exit(0 if result['health'] else 1)
