#!/usr/bin/env python3
"""
MOTHER Status Display
Generates status message to be displayed in all Manus project outputs
Shows enforcement status without generating additional operational costs
"""

import os
import json
from pathlib import Path
from datetime import datetime

class MOTHERStatusDisplay:
    def __init__(self):
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.version_file = self.base_path / "VERSION"
        self.enforcement_checks = {
            'P1_study_first': False,
            'P2_decide_autonomously': False,
            'P3_optimize_cost': False,
            'P4_ensure_quality': False,
            'P5_report_accurately': False,
            'scientific_method': False,
            'bibliographic_refs': False,
            'annas_archive': False,
            'cost_reporting': False,
            'visual_identity': False,
            'guardian_validation': False
        }
    
    def check_enforcement_status(self):
        """Check which enforcements are loaded"""
        
        # Check P1-P5 (Operating System)
        os_file = self.base_path / "core" / "OPERATING_SYSTEM_V2.md"
        if os_file.exists():
            self.enforcement_checks['P1_study_first'] = True
            self.enforcement_checks['P2_decide_autonomously'] = True
            self.enforcement_checks['P3_optimize_cost'] = True
            self.enforcement_checks['P4_ensure_quality'] = True
            self.enforcement_checks['P5_report_accurately'] = True
        
        # Check Scientific Method
        sci_file = self.base_path / "core" / "SCIENTIFIC_METHODOLOGY_REQUIREMENTS.md"
        if sci_file.exists():
            self.enforcement_checks['scientific_method'] = True
            self.enforcement_checks['bibliographic_refs'] = True
        
        # Check Anna's Archive
        annas_file = self.base_path / "core" / "annas_archive_workflow.py"
        if annas_file.exists():
            self.enforcement_checks['annas_archive'] = True
        
        # Check Cost Reporting
        cost_file = self.base_path / "core" / "auto_cost_reporter.py"
        if cost_file.exists():
            self.enforcement_checks['cost_reporting'] = True
        
        # Check Visual Identity
        visual_file = self.base_path / "core" / "visual_identity_detector.py"
        if visual_file.exists():
            self.enforcement_checks['visual_identity'] = True
        
        # Check Guardian Validation
        guardian_file = self.base_path / "core" / "quality_guardian.py"
        if guardian_file.exists():
            self.enforcement_checks['guardian_validation'] = True
    
    def get_version(self):
        """Get MOTHER version"""
        try:
            if self.version_file.exists():
                return self.version_file.read_text().strip()
            return "Unknown"
        except:
            return "Unknown"
    
    def calculate_compliance(self):
        """Calculate overall compliance percentage"""
        total = len(self.enforcement_checks)
        active = sum(1 for v in self.enforcement_checks.values() if v)
        return int((active / total) * 100)
    
    def generate_compact_status(self):
        """Generate compact status message for every output"""
        self.check_enforcement_status()
        version = self.get_version()
        compliance = self.calculate_compliance()
        
        # Status indicator
        if compliance == 100:
            status_icon = "✅"
            status_text = "FULL"
        elif compliance >= 80:
            status_icon = "⚠️"
            status_text = "PARTIAL"
        else:
            status_icon = "❌"
            status_text = "LIMITED"
        
        # Compact one-liner
        message = f"{status_icon} MOTHER v{version} | Enforcement: {status_text} ({compliance}%) | P1-P5: {'✓' if all([self.enforcement_checks['P1_study_first'], self.enforcement_checks['P2_decide_autonomously'], self.enforcement_checks['P3_optimize_cost'], self.enforcement_checks['P4_ensure_quality'], self.enforcement_checks['P5_report_accurately']]) else '✗'} | Scientific: {'✓' if self.enforcement_checks['scientific_method'] else '✗'} | Guardian: {'✓' if self.enforcement_checks['guardian_validation'] else '✗'} | Cost: {'✓' if self.enforcement_checks['cost_reporting'] else '✗'}"
        
        return message
    
    def generate_detailed_status(self):
        """Generate detailed status message for task start"""
        self.check_enforcement_status()
        version = self.get_version()
        compliance = self.calculate_compliance()
        
        # Header
        lines = []
        lines.append("┌" + "─"*78 + "┐")
        lines.append("│" + " "*24 + f"🤖 MOTHER v{version} STATUS" + " "*(28-len(version)) + "│")
        lines.append("├" + "─"*78 + "┤")
        
        # Compliance
        if compliance == 100:
            status = "✅ FULL COMPLIANCE"
            color = ""
        elif compliance >= 80:
            status = "⚠️  PARTIAL COMPLIANCE"
            color = ""
        else:
            status = "❌ LIMITED COMPLIANCE"
            color = ""
        
        lines.append(f"│  Enforcement Status: {status}" + " "*(56-len(status)) + "│")
        lines.append(f"│  Compliance: {compliance}%" + " "*64 + "│")
        lines.append("├" + "─"*78 + "┤")
        
        # Core Principles (P1-P5)
        lines.append("│  Core Principles (P1-P5):" + " "*50 + "│")
        principles = [
            ("P1: Always Study First", self.enforcement_checks['P1_study_first']),
            ("P2: Always Decide Autonomously", self.enforcement_checks['P2_decide_autonomously']),
            ("P3: Always Optimize Cost", self.enforcement_checks['P3_optimize_cost']),
            ("P4: Always Ensure Quality", self.enforcement_checks['P4_ensure_quality']),
            ("P5: Always Report Accurately", self.enforcement_checks['P5_report_accurately'])
        ]
        
        for principle, status in principles:
            icon = "✓" if status else "✗"
            lines.append(f"│    {icon} {principle}" + " "*(72-len(principle)) + "│")
        
        lines.append("├" + "─"*78 + "┤")
        
        # Additional Enforcements
        lines.append("│  Additional Enforcements:" + " "*51 + "│")
        additional = [
            ("Scientific Method (12 steps)", self.enforcement_checks['scientific_method']),
            ("Bibliographic References", self.enforcement_checks['bibliographic_refs']),
            ("Anna's Archive Integration", self.enforcement_checks['annas_archive']),
            ("Cost Reporting", self.enforcement_checks['cost_reporting']),
            ("Visual Identity Detection", self.enforcement_checks['visual_identity']),
            ("Guardian Validation (≥80%)", self.enforcement_checks['guardian_validation'])
        ]
        
        for item, status in additional:
            icon = "✓" if status else "✗"
            lines.append(f"│    {icon} {item}" + " "*(72-len(item)) + "│")
        
        # Footer
        lines.append("├" + "─"*78 + "┤")
        lines.append("│  " + "\"Somente unidos seremos mais fortes!\"" + " "*37 + "│")
        lines.append("└" + "─"*78 + "┘")
        
        return "\n".join(lines)
    
    def save_status_to_file(self, output_path="/tmp/mother_status.txt"):
        """Save status to file for easy inclusion"""
        compact = self.generate_compact_status()
        detailed = self.generate_detailed_status()
        
        with open(output_path, 'w') as f:
            f.write("# MOTHER Status\n\n")
            f.write("## Compact (for every output)\n")
            f.write(f"```\n{compact}\n```\n\n")
            f.write("## Detailed (for task start)\n")
            f.write(f"```\n{detailed}\n```\n")
        
        return output_path

def display_compact():
    """Quick function to display compact status"""
    display = MOTHERStatusDisplay()
    print(display.generate_compact_status())

def display_detailed():
    """Quick function to display detailed status"""
    display = MOTHERStatusDisplay()
    print(display.generate_detailed_status())

def main():
    """Main function"""
    import sys
    
    display = MOTHERStatusDisplay()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "compact":
            print(display.generate_compact_status())
        elif sys.argv[1] == "detailed":
            print(display.generate_detailed_status())
        elif sys.argv[1] == "save":
            path = display.save_status_to_file()
            print(f"Status saved to: {path}")
        else:
            print("Usage: mother_status_display.py [compact|detailed|save]")
    else:
        # Default: show detailed
        print(display.generate_detailed_status())

if __name__ == "__main__":
    main()
