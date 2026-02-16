#!/usr/bin/env python3
"""
Verification Engine & Integration Monitor - Automated Checks for Guardian System

Implements HRO Principles:
- Principle 4: Explicit Confirmation
- Principle 9: Team-Based Verification
- Principle 12: Continuous Monitoring

This module provides automated verification and continuous health monitoring.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class VerificationResult:
    """Result of a verification check."""
    check_name: str
    passed: bool
    message: str
    details: Optional[str] = None


class VerificationEngine:
    """
    Performs automated verification checks.
    
    Acts as an automated "cross-check" to verify integrations, tests, and
    other critical steps.
    """
    
    def __init__(self):
        """Initialize the Verification Engine."""
        self.results: List[VerificationResult] = []
    
    def verify_file_exists(self, file_path: str, description: str = "") -> VerificationResult:
        """
        Verify that a file exists.
        
        Args:
            file_path: Path to the file
            description: Human-readable description
            
        Returns:
            VerificationResult
        """
        path = Path(file_path).expanduser()
        passed = path.exists()
        
        if passed:
            message = f"✓ File exists: {description or file_path}"
        else:
            message = f"✗ File missing: {description or file_path}"
        
        result = VerificationResult(
            check_name=f"file_exists_{path.name}",
            passed=passed,
            message=message,
            details=str(path)
        )
        self.results.append(result)
        return result
    
    def verify_command_succeeds(self, command: str, description: str = "") -> VerificationResult:
        """
        Verify that a shell command succeeds (exit code 0).
        
        Args:
            command: Shell command to run
            description: Human-readable description
            
        Returns:
            VerificationResult
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            passed = result.returncode == 0
            
            if passed:
                message = f"✓ Command succeeded: {description or command}"
            else:
                message = f"✗ Command failed: {description or command}"
            
            details = f"Exit code: {result.returncode}\nStdout: {result.stdout[:200]}\nStderr: {result.stderr[:200]}"
            
        except subprocess.TimeoutExpired:
            passed = False
            message = f"✗ Command timed out: {description or command}"
            details = "Timeout after 30 seconds"
        except Exception as e:
            passed = False
            message = f"✗ Command error: {description or command}"
            details = str(e)
        
        result_obj = VerificationResult(
            check_name=f"command_{description.replace(' ', '_')}",
            passed=passed,
            message=message,
            details=details
        )
        self.results.append(result_obj)
        return result_obj
    
    def verify_python_import(self, module_name: str) -> VerificationResult:
        """
        Verify that a Python module can be imported.
        
        Args:
            module_name: Name of the module to import
            
        Returns:
            VerificationResult
        """
        try:
            __import__(module_name)
            passed = True
            message = f"✓ Python module imports: {module_name}"
            details = None
        except ImportError as e:
            passed = False
            message = f"✗ Python module import failed: {module_name}"
            details = str(e)
        
        result = VerificationResult(
            check_name=f"python_import_{module_name}",
            passed=passed,
            message=message,
            details=details
        )
        self.results.append(result)
        return result
    
    def verify_env_var_set(self, var_name: str) -> VerificationResult:
        """
        Verify that an environment variable is set.
        
        Args:
            var_name: Name of the environment variable
            
        Returns:
            VerificationResult
        """
        value = os.environ.get(var_name)
        passed = value is not None and value != ""
        
        if passed:
            message = f"✓ Environment variable set: {var_name}"
            details = f"Value: {value[:20]}..." if len(value) > 20 else f"Value: {value}"
        else:
            message = f"✗ Environment variable not set: {var_name}"
            details = None
        
        result = VerificationResult(
            check_name=f"env_var_{var_name}",
            passed=passed,
            message=message,
            details=details
        )
        self.results.append(result)
        return result
    
    def run_all_checks(self, checks: List[callable]) -> Tuple[bool, str]:
        """
        Run a list of verification checks.
        
        Args:
            checks: List of callable verification methods
            
        Returns:
            (all_passed, summary) tuple
        """
        self.results = []  # Reset results
        
        for check in checks:
            check()
        
        all_passed = all(r.passed for r in self.results)
        passed_count = sum(1 for r in self.results if r.passed)
        total_count = len(self.results)
        
        summary = f"Verification: {passed_count}/{total_count} checks passed\n\n"
        for result in self.results:
            summary += f"{result.message}\n"
            if result.details and not result.passed:
                summary += f"  Details: {result.details}\n"
        
        return all_passed, summary
    
    def get_failed_checks(self) -> List[VerificationResult]:
        """
        Get all failed verification checks.
        
        Returns:
            List of failed VerificationResults
        """
        return [r for r in self.results if not r.passed]


class IntegrationMonitor:
    """
    Continuously monitors the health and integration status of core systems.
    
    Provides continuous monitoring (Principle 12) to detect silent failures.
    """
    
    def __init__(self):
        """Initialize the Integration Monitor."""
        self.health_status: Dict[str, bool] = {}
    
    def check_compliance_system(self) -> Tuple[bool, str]:
        """
        Check if the compliance system is active.
        
        Returns:
            (is_active, message) tuple
        """
        # Check if compliance engine file exists
        compliance_file = Path("~/manus_global_knowledge/mother_v5/compliance/compliance_engine.py").expanduser()
        
        if not compliance_file.exists():
            return False, "✗ Compliance system not found"
        
        # Check if it can be imported
        try:
            import sys
            sys.path.insert(0, str(compliance_file.parent))
            import compliance_engine
            return True, "✓ Compliance system active"
        except ImportError as e:
            return False, f"✗ Compliance system import failed: {e}"
    
    def check_api_keys(self) -> Tuple[bool, str]:
        """
        Check if API keys are loaded.
        
        Returns:
            (are_loaded, message) tuple
        """
        required_keys = ['OPENAI_API_KEY', 'APOLLO_API_KEY']
        missing_keys = [key for key in required_keys if not os.environ.get(key)]
        
        if missing_keys:
            return False, f"✗ Missing API keys: {', '.join(missing_keys)}"
        
        return True, "✓ All API keys loaded"
    
    def check_cost_optimizer(self) -> Tuple[bool, str]:
        """
        Check if cost optimization system is integrated.
        
        Returns:
            (is_integrated, message) tuple
        """
        # Check if cost optimization files exist
        optimizer_file = Path("~/manus_global_knowledge/core/prompt_optimizer.py").expanduser()
        
        if not optimizer_file.exists():
            return False, "✗ Cost optimizer not found"
        
        return True, "✓ Cost optimizer present"
    
    def check_api_key_manager(self) -> Tuple[bool, str]:
        """
        Check if API Key Manager is active.
        
        Returns:
            (is_active, message) tuple
        """
        manager_file = Path("~/manus_global_knowledge/core/api_key_manager.py").expanduser()
        secrets_file = Path("~/.manus_secrets.enc").expanduser()
        
        if not manager_file.exists():
            return False, "✗ API Key Manager not found"
        
        if not secrets_file.exists():
            return False, "✗ API keys not saved (no secrets file)"
        
        return True, "✓ API Key Manager active"
    
    def check_all(self) -> Tuple[bool, str]:
        """
        Check all core systems.
        
        Returns:
            (all_healthy, report) tuple
        """
        checks = [
            ('Compliance System', self.check_compliance_system),
            ('API Keys', self.check_api_keys),
            ('Cost Optimizer', self.check_cost_optimizer),
            ('API Key Manager', self.check_api_key_manager)
        ]
        
        results = []
        all_healthy = True
        
        for name, check_func in checks:
            is_healthy, message = check_func()
            self.health_status[name] = is_healthy
            results.append(message)
            if not is_healthy:
                all_healthy = False
        
        report = "Integration Monitor Health Check:\n\n"
        report += "\n".join(results)
        report += f"\n\nOverall: {'✓ All systems healthy' if all_healthy else '✗ Some systems unhealthy'}"
        
        return all_healthy, report
    
    def get_unhealthy_systems(self) -> List[str]:
        """
        Get list of unhealthy systems.
        
        Returns:
            List of system names that are unhealthy
        """
        return [name for name, healthy in self.health_status.items() if not healthy]


if __name__ == "__main__":
    print("Testing VerificationEngine...")
    
    engine = VerificationEngine()
    
    # Test file verification
    engine.verify_file_exists("/home/ubuntu/manus_global_knowledge/bootstrap.sh", "Bootstrap script")
    engine.verify_file_exists("/nonexistent/file.txt", "Nonexistent file")
    
    # Test command verification
    engine.verify_command_succeeds("echo 'test'", "Echo test")
    engine.verify_command_succeeds("false", "False command (should fail)")
    
    # Test environment variable
    os.environ['TEST_VAR'] = 'test_value'
    engine.verify_env_var_set('TEST_VAR')
    engine.verify_env_var_set('NONEXISTENT_VAR')
    
    # Print results
    print("\nVerification Results:")
    for result in engine.results:
        print(f"  {result.message}")
    
    print(f"\nFailed checks: {len(engine.get_failed_checks())}")
    
    print("\n" + "="*50)
    print("\nTesting IntegrationMonitor...")
    
    monitor = IntegrationMonitor()
    all_healthy, report = monitor.check_all()
    
    print(report)
    
    if not all_healthy:
        print(f"\nUnhealthy systems: {monitor.get_unhealthy_systems()}")
    
    print("\n✅ Verification module test complete!")
