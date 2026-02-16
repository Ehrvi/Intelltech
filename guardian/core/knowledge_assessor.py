#!/usr/bin/env python3
"""
Knowledge Assessor - Pre-Task Knowledge Assessment System
Part of the Guardian System for ensuring 100% AI reliability

Purpose: Identify required knowledge areas and assess current knowledge level
"""

import json
import os
from typing import List, Dict, Tuple
from pathlib import Path

class KnowledgeAssessor:
    """Assesses knowledge level for specific areas before task execution."""
    
    def __init__(self):
        """Initialize the Knowledge Assessor."""
        self.expertise_file = Path(__file__).parent / "self_expertise.json"
        self.expertise = self._load_expertise()
    
    def _load_expertise(self) -> Dict[str, str]:
        """Load the self-expertise dictionary."""
        if self.expertise_file.exists():
            with open(self.expertise_file, 'r') as f:
                return json.load(f)
        else:
            # Default expertise (will be expanded over time)
            default_expertise = {
                # Programming
                "python_programming": "master",
                "javascript_programming": "master",
                "typescript_programming": "master",
                "react_development": "master",
                "node_development": "master",
                "api_design": "adequate",
                "database_design": "adequate",
                "sql": "adequate",
                
                # AI/ML
                "machine_learning": "adequate",
                "deep_learning": "adequate",
                "natural_language_processing": "adequate",
                "llm_fine_tuning": "gap",
                
                # Systems
                "linux_administration": "adequate",
                "docker_containers": "adequate",
                "kubernetes": "gap",
                "distributed_systems": "adequate",
                
                # Security
                "cryptography_basics": "adequate",
                "api_key_management": "adequate",
                "penetration_testing": "gap",
                
                # Specialized
                "blockchain_consensus": "gap",
                "quantum_computing": "gap",
                "formal_verification": "gap",
                "compiler_design": "gap"
            }
            
            # Save default
            self.expertise_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.expertise_file, 'w') as f:
                json.dump(default_expertise, f, indent=2)
            
            return default_expertise
    
    def identify_required_areas(self, task_description: str) -> List[str]:
        """
        Identify required knowledge areas from task description.
        
        Uses keyword matching and domain mapping to identify 3-5 key areas.
        In production, this could use an LLM call for better accuracy.
        
        Args:
            task_description: The task description from the user
            
        Returns:
            List of knowledge area identifiers
        """
        task_lower = task_description.lower()
        required_areas = []
        
        # Domain mapping (keywords -> knowledge areas)
        domain_map = {
            # Programming
            "python": "python_programming",
            "javascript": "javascript_programming",
            "typescript": "typescript_programming",
            "react": "react_development",
            "node": "node_development",
            "api": "api_design",
            "database": "database_design",
            "sql": "sql",
            
            # AI/ML
            "machine learning": "machine_learning",
            "ml": "machine_learning",
            "deep learning": "deep_learning",
            "neural network": "deep_learning",
            "nlp": "natural_language_processing",
            "language model": "natural_language_processing",
            "fine-tun": "llm_fine_tuning",
            
            # Systems
            "linux": "linux_administration",
            "docker": "docker_containers",
            "kubernetes": "kubernetes",
            "k8s": "kubernetes",
            "distributed": "distributed_systems",
            
            # Security
            "cryptography": "cryptography_basics",
            "encryption": "cryptography_basics",
            "api key": "api_key_management",
            "secret": "api_key_management",
            "penetration test": "penetration_testing",
            "security audit": "penetration_testing",
            
            # Specialized
            "blockchain": "blockchain_consensus",
            "consensus": "blockchain_consensus",
            "quantum": "quantum_computing",
            "formal verification": "formal_verification",
            "compiler": "compiler_design"
        }
        
        # Check for keyword matches
        for keyword, area in domain_map.items():
            if keyword in task_lower and area not in required_areas:
                required_areas.append(area)
        
        # If no matches, assume general programming
        if not required_areas:
            required_areas.append("python_programming")
        
        return required_areas[:5]  # Max 5 areas
    
    def assess_knowledge_level(self, area: str) -> str:
        """
        Assess knowledge level for a specific area.
        
        Args:
            area: Knowledge area identifier
            
        Returns:
            "master" | "adequate" | "gap"
        """
        return self.expertise.get(area, "gap")
    
    def generate_assessment_report(self, 
                                   task_description: str,
                                   assessments: Dict[str, str]) -> str:
        """
        Generate a formatted assessment report for the user.
        
        Args:
            task_description: The original task
            assessments: Dict of {area: level}
            
        Returns:
            Formatted Markdown report
        """
        # Count gaps
        gaps = [area for area, level in assessments.items() if level == "gap"]
        adequate = [area for area, level in assessments.items() if level == "adequate"]
        master = [area for area, level in assessments.items() if level == "master"]
        
        # Generate report
        report = ["## 🔍 Pre-Task Knowledge Assessment\n"]
        report.append(f"**Task:** {task_description[:100]}...\n")
        report.append("### Knowledge Areas Required\n")
        
        # Master level
        if master:
            report.append("**✅ Master Level:**")
            for area in master:
                report.append(f"- {area.replace('_', ' ').title()}")
            report.append("")
        
        # Adequate level
        if adequate:
            report.append("**⚠️ Adequate Level:**")
            for area in adequate:
                report.append(f"- {area.replace('_', ' ').title()}")
            report.append("")
        
        # Gaps
        if gaps:
            report.append("**❌ Knowledge Gaps:**")
            for area in gaps:
                report.append(f"- {area.replace('_', ' ').title()}")
            report.append("")
        
        # Recommendation
        report.append("### Recommendation\n")
        if not gaps:
            report.append("✅ **Proceed:** All required knowledge areas are at adequate or master level.")
        elif len(gaps) <= 2:
            report.append(f"⚠️ **Research Recommended:** {len(gaps)} knowledge gap(s) identified. "
                         "Research is recommended before implementation.")
        else:
            report.append(f"🚨 **Research Required:** {len(gaps)} significant knowledge gaps identified. "
                         "Research is strongly recommended before proceeding.")
        
        return "\n".join(report)
    
    def assess_task(self, task_description: str) -> Tuple[Dict[str, str], str]:
        """
        Complete assessment workflow for a task.
        
        Args:
            task_description: The task description
            
        Returns:
            Tuple of (assessments dict, report string)
        """
        # Identify areas
        areas = self.identify_required_areas(task_description)
        
        # Assess each area
        assessments = {area: self.assess_knowledge_level(area) for area in areas}
        
        # Generate report
        report = self.generate_assessment_report(task_description, assessments)
        
        return assessments, report


# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    assessor = KnowledgeAssessor()
    
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = "Create a blockchain consensus algorithm using quantum cryptography"
    
    assessments, report = assessor.assess_task(task)
    print(report)
    print("\n### Raw Assessments:")
    for area, level in assessments.items():
        print(f"  {area}: {level}")
