#!/usr/bin/env python3
"""
Research Planner - Pre-Task Knowledge Assessment System
Part of the Guardian System for ensuring 100% AI reliability

Purpose: Create actionable research plans for identified knowledge gaps
"""

from typing import List, Dict, Tuple
from datetime import datetime

class ResearchPlanner:
    """Creates structured research plans for knowledge gaps."""
    
    def __init__(self):
        """Initialize the Research Planner."""
        self.tier1_sources = [
            ("arXiv.org", "https://arxiv.org/search/?query={}"),
            ("PubMed Central", "https://pubmed.ncbi.nlm.nih.gov/?term={}"),
            ("Google Scholar", "https://scholar.google.com/scholar?q={}"),
            ("DOAJ", "https://doaj.org/search/articles?ref=homepage-box&source=%7B%22query%22%3A%7B%22query_string%22%3A%7B%22query%22%3A%22{}%22%7D%7D%7D"),
            ("Internet Archive", "https://archive.org/search.php?query={}")
        ]
        
        self.tier2_sources = [
            ("ResearchGate", "https://www.researchgate.net/search/publication?q={}"),
            ("Academia.edu", "https://www.academia.edu/search?q={}")
        ]
    
    def prioritize_sources(self, topic: str, type: str = "paper") -> List[Tuple[str, str]]:
        """
        Return ordered list of research sources based on tiered priority.
        
        Args:
            topic: The research topic
            type: "paper" or "book"
            
        Returns:
            List of (source_name, url) tuples
        """
        sources = []
        
        # Tier 1: Legal and Free
        for name, url_template in self.tier1_sources:
            sources.append((name, url_template.format(topic.replace(" ", "+"))))
        
        # Tier 2: Institutional (if available)
        for name, url_template in self.tier2_sources:
            sources.append((name, url_template.format(topic.replace(" ", "+"))))
        
        # Tier 3: Shadow Libraries (handled by AnnaArchiveIntegration)
        # Will be added by create_research_plan()
        
        return sources
    
    def estimate_research_time(self, num_gaps: int) -> str:
        """
        Estimate research time based on number of gaps.
        
        Args:
            num_gaps: Number of knowledge gaps
            
        Returns:
            Time estimate string
        """
        if num_gaps == 1:
            return "1-2 hours"
        elif num_gaps == 2:
            return "2-3 hours"
        elif num_gaps <= 4:
            return "3-5 hours"
        else:
            return "5-8 hours"
    
    def create_research_plan(self, gaps: List[str]) -> Dict:
        """
        Create a structured research plan for knowledge gaps.
        
        Args:
            gaps: List of knowledge area identifiers with gaps
            
        Returns:
            Research plan dictionary
        """
        plan = {
            "created_at": datetime.now().isoformat(),
            "num_gaps": len(gaps),
            "estimated_time": self.estimate_research_time(len(gaps)),
            "gaps": []
        }
        
        for gap in gaps:
            # Convert identifier to readable topic
            topic = gap.replace("_", " ")
            
            # Get prioritized sources
            sources = self.prioritize_sources(topic)
            
            gap_plan = {
                "area": gap,
                "topic": topic.title(),
                "sources": sources,
                "recommended_papers": 3,  # Read at least 3 papers per gap
                "notes": self._get_research_notes(gap)
            }
            
            plan["gaps"].append(gap_plan)
        
        return plan
    
    def _get_research_notes(self, area: str) -> str:
        """
        Get area-specific research notes.
        
        Args:
            area: Knowledge area identifier
            
        Returns:
            Research guidance string
        """
        notes_map = {
            "blockchain_consensus": "Focus on: Nakamoto consensus, PBFT, Raft. Compare trade-offs.",
            "kubernetes": "Focus on: Architecture, pod management, service discovery, scaling.",
            "quantum_computing": "Focus on: Qubits, quantum gates, quantum algorithms (Shor, Grover).",
            "formal_verification": "Focus on: Model checking, theorem proving, Z notation, TLA+.",
            "compiler_design": "Focus on: Lexical analysis, parsing, optimization, code generation.",
            "llm_fine_tuning": "Focus on: LoRA, QLoRA, full fine-tuning, dataset preparation.",
            "penetration_testing": "Focus on: OWASP Top 10, common vulnerabilities, testing methodologies."
        }
        
        return notes_map.get(area, "Focus on: Fundamentals, best practices, recent advances.")
    
    def generate_research_plan_report(self, plan: Dict) -> str:
        """
        Generate a formatted research plan report.
        
        Args:
            plan: Research plan dictionary
            
        Returns:
            Formatted Markdown report
        """
        report = ["## 📚 Research Plan\n"]
        report.append(f"**Estimated Time:** {plan['estimated_time']}")
        report.append(f"**Knowledge Gaps:** {plan['num_gaps']}\n")
        
        for i, gap_plan in enumerate(plan['gaps'], 1):
            report.append(f"### {i}. {gap_plan['topic']}\n")
            report.append(f"**Guidance:** {gap_plan['notes']}\n")
            report.append(f"**Recommended:** Read at least {gap_plan['recommended_papers']} papers/articles\n")
            report.append("**Sources (in priority order):**\n")
            
            # Show top 5 sources
            for j, (name, url) in enumerate(gap_plan['sources'][:5], 1):
                report.append(f"{j}. [{name}]({url})")
            
            report.append("")  # Blank line
        
        # Add Anna's Archive note
        report.append("---\n")
        report.append("**Note:** If papers are not available in the above sources, "
                     "Anna's Archive will be checked as a last resort. "
                     "Legal alternatives are always prioritized.\n")
        
        return "\n".join(report)


# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    planner = ResearchPlanner()
    
    if len(sys.argv) > 1:
        gaps = sys.argv[1:]
    else:
        gaps = ["kubernetes", "blockchain_consensus"]
    
    plan = planner.create_research_plan(gaps)
    report = planner.generate_research_plan_report(plan)
    print(report)
