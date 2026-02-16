#!/usr/bin/env python3
"""
MANDATORY SCIENTIFIC ENFORCEMENT SYSTEM
Enforces Anna's Archive usage and 12-step scientific method for ALL outputs
Version: 1.0
Status: CRITICAL - BLOCKING
"""

import os
import sys
from datetime import datetime

class ScientificEnforcement:
    """Enforces scientific methodology and Anna's Archive usage"""
    
    def __init__(self):
        self.violations = []
        self.warnings = []
        self.compliance_score = 100.0
        
    def check_annas_archive_usage(self, research_log: dict) -> bool:
        """
        Check if Anna's Archive was consulted for academic research
        
        Args:
            research_log: Dict with research sources used
            
        Returns:
            bool: True if compliant, False if violation
        """
        requires_academic = research_log.get('requires_academic_papers', False)
        used_annas = research_log.get('used_annas_archive', False)
        
        if requires_academic and not used_annas:
            self.violations.append({
                'type': 'CRITICAL',
                'rule': 'Anna\'s Archive Usage',
                'message': 'Academic research required but Anna\'s Archive not used',
                'impact': -20.0
            })
            self.compliance_score -= 20.0
            return False
        
        return True
    
    def check_scientific_method_steps(self, execution_log: dict) -> bool:
        """
        Check if 12-step scientific method was followed
        
        Args:
            execution_log: Dict with steps executed
            
        Returns:
            bool: True if compliant, False if violation
        """
        required_steps = [
            'study_internal_knowledge',
            'research_externally',
            'understand_deeply',
            'define_problem',
            'formulate_hypothesis',
            'design_method',
            'collect_data',
            'process_data',
            'validate_results',
            'synthesize_findings',
            'document_results',
            'report_to_user'
        ]
        
        completed_steps = execution_log.get('completed_steps', [])
        missing_steps = [s for s in required_steps if s not in completed_steps]
        
        if missing_steps:
            self.violations.append({
                'type': 'CRITICAL',
                'rule': '12-Step Scientific Method',
                'message': f'Missing steps: {", ".join(missing_steps)}',
                'impact': -15.0 * len(missing_steps)
            })
            self.compliance_score -= (15.0 * len(missing_steps))
            return False
        
        return True
    
    def check_bibliographic_references(self, output_text: str) -> bool:
        """
        Check if output includes bibliographic references
        
        Args:
            output_text: The output text to check
            
        Returns:
            bool: True if compliant, False if violation
        """
        has_claims = any(keyword in output_text.lower() for keyword in [
            'research', 'study', 'according to', 'demonstrates', 
            'shows that', 'evidence', 'findings', 'statistics'
        ])
        
        has_references = '[1]' in output_text or 'References:' in output_text
        
        if has_claims and not has_references:
            self.violations.append({
                'type': 'CRITICAL',
                'rule': 'Bibliographic References',
                'message': 'Scientific claims made without citations',
                'impact': -25.0
            })
            self.compliance_score -= 25.0
            return False
        
        return True
    
    def check_guardian_validation(self, output_type: str, guardian_score: float = None) -> bool:
        """
        Check if Guardian validation was used for permanent knowledge
        
        Args:
            output_type: Type of output (permanent/temporary)
            guardian_score: Guardian quality score (if used)
            
        Returns:
            bool: True if compliant, False if violation
        """
        if output_type == 'permanent':
            if guardian_score is None:
                self.violations.append({
                    'type': 'CRITICAL',
                    'rule': 'Guardian Validation',
                    'message': 'Permanent knowledge created without Guardian validation',
                    'impact': -30.0
                })
                self.compliance_score -= 30.0
                return False
            
            if guardian_score < 80.0:
                self.violations.append({
                    'type': 'CRITICAL',
                    'rule': 'Guardian Quality Score',
                    'message': f'Guardian score {guardian_score}% < 80% minimum',
                    'impact': -20.0
                })
                self.compliance_score -= 20.0
                return False
        
        return True
    
    def enforce_all(self, task_context: dict) -> dict:
        """
        Run all enforcement checks
        
        Args:
            task_context: Dict with task execution details
            
        Returns:
            dict: Enforcement result
        """
        self.violations = []
        self.warnings = []
        self.compliance_score = 100.0
        
        # Check Anna's Archive usage
        research_log = task_context.get('research_log', {})
        annas_ok = self.check_annas_archive_usage(research_log)
        
        # Check scientific method
        execution_log = task_context.get('execution_log', {})
        method_ok = self.check_scientific_method_steps(execution_log)
        
        # Check bibliographic references
        output_text = task_context.get('output_text', '')
        refs_ok = self.check_bibliographic_references(output_text)
        
        # Check Guardian validation
        output_type = task_context.get('output_type', 'temporary')
        guardian_score = task_context.get('guardian_score')
        guardian_ok = self.check_guardian_validation(output_type, guardian_score)
        
        # Determine overall compliance
        all_ok = annas_ok and method_ok and refs_ok and guardian_ok
        
        return {
            'compliant': all_ok,
            'compliance_score': max(0.0, self.compliance_score),
            'violations': self.violations,
            'warnings': self.warnings,
            'checks': {
                'annas_archive': annas_ok,
                'scientific_method': method_ok,
                'bibliographic_references': refs_ok,
                'guardian_validation': guardian_ok
            }
        }
    
    def generate_report(self, result: dict) -> str:
        """Generate enforcement report"""
        report = []
        report.append("╔" + "="*78 + "╗")
        report.append("║" + " "*20 + "🔬 SCIENTIFIC ENFORCEMENT REPORT" + " "*26 + "║")
        report.append("╠" + "="*78 + "╣")
        
        # Compliance score
        score = result['compliance_score']
        status = "✅ PASS" if result['compliant'] else "❌ FAIL"
        report.append(f"║  Compliance Score: {score:.1f}% - {status}" + " "*(78-len(f"  Compliance Score: {score:.1f}% - {status}")) + "║")
        report.append("║" + " "*78 + "║")
        
        # Individual checks
        report.append("║  Individual Checks:" + " "*59 + "║")
        for check_name, check_ok in result['checks'].items():
            status_icon = "✅" if check_ok else "❌"
            check_label = check_name.replace('_', ' ').title()
            line = f"║    {status_icon} {check_label}"
            report.append(line + " "*(78-len(line)+2) + "║")
        
        # Violations
        if result['violations']:
            report.append("║" + " "*78 + "║")
            report.append("║  🚨 VIOLATIONS:" + " "*63 + "║")
            for v in result['violations']:
                line = f"║    [{v['type']}] {v['rule']}: {v['message']}"
                if len(line) > 78:
                    line = line[:75] + "..."
                report.append(line + " "*(78-len(line)+2) + "║")
        
        report.append("╚" + "="*78 + "╝")
        return "\n".join(report)


def enforce_scientific_standards(task_context: dict) -> dict:
    """
    Main enforcement function
    
    Args:
        task_context: Task execution context
        
    Returns:
        Enforcement result
    """
    enforcer = ScientificEnforcement()
    result = enforcer.enforce_all(task_context)
    
    # Print report
    print(enforcer.generate_report(result))
    
    # Block if not compliant
    if not result['compliant']:
        print("\n🚨 CRITICAL: Task does not meet scientific standards!")
        print("   Please revise to ensure compliance before proceeding.\n")
    
    return result


# CLI for testing
if __name__ == "__main__":
    # Test case 1: Compliant task
    print("TEST 1: Compliant Task")
    print("="*80)
    
    compliant_context = {
        'research_log': {
            'requires_academic_papers': True,
            'used_annas_archive': True
        },
        'execution_log': {
            'completed_steps': [
                'study_internal_knowledge',
                'research_externally',
                'understand_deeply',
                'define_problem',
                'formulate_hypothesis',
                'design_method',
                'collect_data',
                'process_data',
                'validate_results',
                'synthesize_findings',
                'document_results',
                'report_to_user'
            ]
        },
        'output_text': 'Research demonstrates that X is Y.[1]\n\n[1] Author (2026). "Title." Journal.',
        'output_type': 'permanent',
        'guardian_score': 85.0
    }
    
    result1 = enforce_scientific_standards(compliant_context)
    
    print("\n\n")
    
    # Test case 2: Non-compliant task
    print("TEST 2: Non-Compliant Task")
    print("="*80)
    
    noncompliant_context = {
        'research_log': {
            'requires_academic_papers': True,
            'used_annas_archive': False  # VIOLATION
        },
        'execution_log': {
            'completed_steps': [
                'study_internal_knowledge',
                'collect_data',
                'report_to_user'
                # Missing 9 steps - VIOLATION
            ]
        },
        'output_text': 'Research shows that X is Y.',  # No citations - VIOLATION
        'output_type': 'permanent',
        'guardian_score': None  # No Guardian - VIOLATION
    }
    
    result2 = enforce_scientific_standards(noncompliant_context)
