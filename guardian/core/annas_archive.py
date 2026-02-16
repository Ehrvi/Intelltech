#!/usr/bin/env python3
"""
Anna's Archive Integration - Pre-Task Knowledge Assessment System
Part of the Guardian System for ensuring 100% AI reliability

Purpose: Provide resilient interface to Anna's Archive with fallback handling
"""

import requests
from typing import Optional, Dict, List
from datetime import datetime, timedelta

class AnnaArchiveIntegration:
    """Handles Anna's Archive access with mirror and fallback support."""
    
    def __init__(self):
        """Initialize the Anna's Archive integration."""
        self.known_domains = [
            "annas-archive.li",
            "annas-archive.gl",
            "annas-archive.pm"
        ]
        self.current_domain = None
        self.last_check = None
        self.check_interval = timedelta(hours=1)  # Re-check every hour
    
    def get_current_domain(self) -> Optional[str]:
        """
        Check which Anna's Archive domain is currently accessible.
        
        Returns:
            Working domain string or None if all are down
        """
        # Use cached result if recent
        if (self.current_domain and self.last_check and 
            datetime.now() - self.last_check < self.check_interval):
            return self.current_domain
        
        # Check each domain
        for domain in self.known_domains:
            if self._is_accessible(domain):
                self.current_domain = domain
                self.last_check = datetime.now()
                return domain
        
        # All domains down
        self.current_domain = None
        self.last_check = datetime.now()
        return None
    
    def _is_accessible(self, domain: str) -> bool:
        """
        Check if a domain is accessible.
        
        Args:
            domain: Domain to check
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            response = requests.head(f"https://{domain}", timeout=5)
            return response.status_code < 400
        except:
            return False
    
    def search(self, query: str, type: str = "paper") -> List[Dict]:
        """
        Search Anna's Archive.
        
        Args:
            query: Search query
            type: "paper" or "book"
            
        Returns:
            List of search results (simplified)
        """
        domain = self.get_current_domain()
        
        if not domain:
            return []
        
        # In a real implementation, this would parse the search results
        # For now, return the search URL
        search_url = f"https://{domain}/search?q={query.replace(' ', '+')}"
        
        return [{
            "type": "search_url",
            "url": search_url,
            "note": "Manual search required - automated parsing not implemented"
        }]
    
    def get_fallback_service(self, type: str = "paper") -> Dict:
        """
        Get fallback service when Anna's Archive is down.
        
        Args:
            type: "paper" or "book"
            
        Returns:
            Dictionary with fallback service info
        """
        if type == "paper":
            return {
                "name": "Sci-Hub",
                "domains": ["sci-hub.se", "sci-hub.st", "sci-hub.ru"],
                "instructions": "Use DOI for direct access. Search: https://sci-hub.se/{doi}",
                "search_url": "https://sci-hub.se/"
            }
        elif type == "book":
            return {
                "name": "Library Genesis",
                "domains": ["libgen.is", "libgen.rs", "libgen.st"],
                "instructions": "Search by title, author, or ISBN",
                "search_url": "https://libgen.is/search.php?req={}"
            }
        else:
            return {
                "name": "Internet Archive",
                "domains": ["archive.org"],
                "instructions": "Legal alternative - public domain + 2-hour lending",
                "search_url": "https://archive.org/search.php?query={}"
            }
    
    def get_research_sources(self, topic: str, type: str = "paper") -> List[Dict]:
        """
        Get complete list of research sources including Anna's Archive.
        
        This implements the tiered priority system:
        Tier 1 (Legal/Free) → Tier 2 (Institutional) → Tier 3 (Shadow)
        
        Args:
            topic: Research topic
            type: "paper" or "book"
            
        Returns:
            List of source dictionaries with tier information
        """
        sources = []
        
        # Tier 1: Legal and Free
        sources.append({
            "tier": 1,
            "name": "arXiv.org",
            "url": f"https://arxiv.org/search/?query={topic.replace(' ', '+')}",
            "type": "legal"
        })
        sources.append({
            "tier": 1,
            "name": "Google Scholar",
            "url": f"https://scholar.google.com/scholar?q={topic.replace(' ', '+')}",
            "type": "legal"
        })
        
        if type == "paper":
            sources.append({
                "tier": 1,
                "name": "PubMed Central",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/?term={topic.replace(' ', '+')}",
                "type": "legal"
            })
        
        # Tier 3: Shadow Libraries (Anna's Archive)
        domain = self.get_current_domain()
        
        if domain:
            sources.append({
                "tier": 3,
                "name": "Anna's Archive",
                "url": f"https://{domain}/search?q={topic.replace(' ', '+')}",
                "type": "shadow",
                "note": "Use only if Tier 1-2 sources don't have the material"
            })
        else:
            # Fallback
            fallback = self.get_fallback_service(type)
            sources.append({
                "tier": 3,
                "name": fallback["name"],
                "url": fallback["search_url"].format(topic.replace(' ', '+')),
                "type": "shadow",
                "note": f"Anna's Archive is down. {fallback['instructions']}"
            })
        
        return sources
    
    def generate_usage_report(self) -> str:
        """
        Generate a report on Anna's Archive status and usage instructions.
        
        Returns:
            Formatted Markdown report
        """
        domain = self.get_current_domain()
        
        report = ["## 📖 Anna's Archive Status\n"]
        
        if domain:
            report.append(f"**Status:** ✅ Accessible")
            report.append(f"**Current Domain:** {domain}")
            report.append(f"**Last Checked:** {self.last_check.strftime('%Y-%m-%d %H:%M:%S')}\n")
        else:
            report.append(f"**Status:** ❌ All domains are down")
            report.append(f"**Last Checked:** {self.last_check.strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"**Fallback Services Available:**")
            report.append(f"- Sci-Hub (for papers)")
            report.append(f"- Library Genesis (for books)\n")
        
        report.append("### Usage Instructions\n")
        report.append("**BEFORE using Anna's Archive:**")
        report.append("1. ✅ Check Tier 1 sources (arXiv, PubMed, Google Scholar)")
        report.append("2. ✅ Check Tier 2 sources (institutional access if available)")
        report.append("3. ✅ Only use Anna's Archive if material not found in Tier 1-2\n")
        
        report.append("**IF Anna's Archive is down:**")
        report.append("1. Try all mirrors: .li, .gl, .pm")
        report.append("2. Check Wikipedia for domain updates")
        report.append("3. Use fallback: Sci-Hub (papers) or LibGen (books)\n")
        
        report.append("**Legal Considerations:**")
        report.append("- Anna's Archive is a shadow library (copyright concerns)")
        report.append("- Use for research/learning purposes only")
        report.append("- Prefer legal alternatives when available")
        report.append("- User is responsible for compliance with local laws\n")
        
        return "\n".join(report)


# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    integration = AnnaArchiveIntegration()
    
    # Check status
    print(integration.generate_usage_report())
    
    # Test search if query provided
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"\n### Searching for: {query}\n")
        
        sources = integration.get_research_sources(query, type="paper")
        
        for source in sources:
            print(f"**Tier {source['tier']}: {source['name']}**")
            print(f"URL: {source['url']}")
            if 'note' in source:
                print(f"Note: {source['note']}")
            print()
