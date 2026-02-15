#!/usr/bin/env python3
"""
Mandatory Knowledge Lookup - Fix 5
MUST search existing knowledge before creating new
Prevents reinventing the wheel
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class KnowledgeResult:
    """Represents a knowledge search result"""
    location: str
    relevance_score: float
    excerpt: str
    line_number: Optional[int] = None

class KnowledgeLookup:
    """Searches existing knowledge base"""
    
    def __init__(self):
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.search_locations = [
            self.base_path / "INITIALIZER.md",
            self.base_path / "MASTER_INDEX.md",
            self.base_path / "core",
            self.base_path / "projects",
            self.base_path / "metrics"
        ]
    
    def search_file(self, filepath: Path, keywords: List[str]) -> List[KnowledgeResult]:
        """Search a single file for keywords"""
        
        if not filepath.exists() or not filepath.is_file():
            return []
        
        # Skip binary files
        if filepath.suffix in ['.pyc', '.so', '.o', '.json', '.tar', '.gz']:
            return []
        
        results = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()
                
                # Count keyword matches
                matches = sum(1 for kw in keywords if kw.lower() in line_lower)
                
                if matches > 0:
                    # Calculate relevance score
                    relevance = matches / len(keywords)
                    
                    # Extract excerpt (line + context)
                    start = max(0, line_num - 2)
                    end = min(len(lines), line_num + 2)
                    excerpt = ''.join(lines[start:end]).strip()
                    
                    results.append(KnowledgeResult(
                        location=str(filepath),
                        relevance_score=relevance,
                        excerpt=excerpt[:300],  # Limit excerpt length
                        line_number=line_num
                    ))
        
        except Exception as e:
            # Skip files that can't be read
            pass
        
        return results
    
    def search_directory(self, dirpath: Path, keywords: List[str]) -> List[KnowledgeResult]:
        """Search all files in a directory"""
        
        if not dirpath.exists() or not dirpath.is_dir():
            return []
        
        results = []
        
        for filepath in dirpath.rglob('*'):
            if filepath.is_file():
                file_results = self.search_file(filepath, keywords)
                results.extend(file_results)
        
        return results
    
    def mandatory_lookup(
        self,
        task_description: str,
        min_relevance: float = 0.3
    ) -> Tuple[bool, List[KnowledgeResult]]:
        """
        MANDATORY: Search existing knowledge before proceeding
        
        Args:
            task_description: Description of what you want to create/do
            min_relevance: Minimum relevance score (0-1)
        
        Returns:
            (found, results) - found=True if relevant knowledge exists
        """
        
        # Extract keywords from task description
        keywords = self._extract_keywords(task_description)
        
        all_results = []
        
        # Search all locations
        for location in self.search_locations:
            if location.is_file():
                results = self.search_file(location, keywords)
            elif location.is_dir():
                results = self.search_directory(location, keywords)
            else:
                continue
            
            all_results.extend(results)
        
        # Filter by relevance
        relevant_results = [
            r for r in all_results
            if r.relevance_score >= min_relevance
        ]
        
        # Sort by relevance
        relevant_results.sort(key=lambda r: r.relevance_score, reverse=True)
        
        # Remove duplicates (same file, close line numbers)
        unique_results = self._deduplicate_results(relevant_results)
        
        found = len(unique_results) > 0
        
        return (found, unique_results[:10])  # Return top 10 results
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        
        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Extract words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter stop words and short words
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Return unique keywords
        return list(set(keywords))
    
    def _deduplicate_results(self, results: List[KnowledgeResult]) -> List[KnowledgeResult]:
        """Remove duplicate results from same file"""
        
        seen = set()
        unique = []
        
        for result in results:
            # Create key: file + approximate line number (grouped by 10s)
            line_group = (result.line_number // 10) * 10 if result.line_number else 0
            key = (result.location, line_group)
            
            if key not in seen:
                seen.add(key)
                unique.append(result)
        
        return unique
    
    def print_results(self, results: List[KnowledgeResult]):
        """Print search results in formatted way"""
        
        if not results:
            print("No results found.")
            return
        
        print(f"Found {len(results)} relevant results:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.location}")
            if result.line_number:
                print(f"   Line {result.line_number}")
            print(f"   Relevance: {result.relevance_score*100:.0f}%")
            print(f"   Excerpt: {result.excerpt[:150]}...")
            print()


# Convenience function
def search_knowledge(task_description: str) -> Tuple[bool, List[KnowledgeResult]]:
    """
    Convenience function for searching knowledge
    
    Usage:
        found, results = search_knowledge("initialization system")
        
        if found:
            print(f"Found existing knowledge! Don't create new system.")
            for result in results:
                print(f"  - {result.location}")
        else:
            print("No existing knowledge found. Safe to create new.")
    """
    lookup = KnowledgeLookup()
    return lookup.mandatory_lookup(task_description)


# Test if run directly
if __name__ == "__main__":
    print("="*70)
    print("🔍 MANDATORY KNOWLEDGE LOOKUP - FIX 5")
    print("="*70)
    print()
    
    lookup = KnowledgeLookup()
    
    # Test cases
    test_queries = [
        "initialization system",
        "cost optimization",
        "adaptive router",
        "scientific methodology",
        "completely new unique system that doesn't exist"
    ]
    
    for query in test_queries:
        print(f"Query: '{query}'")
        print("-" * 70)
        
        found, results = lookup.mandatory_lookup(query)
        
        if found:
            print(f"✅ FOUND: Existing knowledge exists!")
            print(f"   {len(results)} relevant results")
            print(f"   Top result: {results[0].location}")
            print(f"   Relevance: {results[0].relevance_score*100:.0f}%")
            print(f"   ❌ DO NOT create new system")
            print(f"   ✅ USE existing knowledge")
        else:
            print(f"❌ NOT FOUND: No existing knowledge")
            print(f"   ✅ Safe to create new system")
        
        print()
    
    # Detailed example
    print("="*70)
    print("📖 DETAILED EXAMPLE: Search for 'initialization'")
    print("="*70)
    print()
    
    found, results = lookup.mandatory_lookup("initialization system")
    lookup.print_results(results)
    
    print("✅ Knowledge lookup working correctly!")
