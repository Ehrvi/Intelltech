#!/usr/bin/env python3
"""
MOTHER V3.3 - Source Verifier

Version: 1.0
Date: 2026-02-16
Status: ACTIVE - CRITICAL ENFORCEMENT
Purpose: To prevent the use of unverified, AI-hallucinated citations.
"""

import re
import os

# This is a placeholder for a real browser history API
# In a real implementation, this would connect to the browser's history database
BROWSER_HISTORY_API = {
    "visited_urls": [
        "https://annas-archive.org/",
        "https://scholar.google.com/",
        "https://www.nature.com/articles/s41586-021-03892-8",
        "https://ieeexplore.ieee.org/document/9637170"
    ]
}

def get_browser_history():
    """Simulates retrieving browser history."""
    return BROWSER_HISTORY_API["visited_urls"]

def find_citations_in_text(text: str) -> list:
    """Finds all numeric citations like [1], [2] in a text."""
    return re.findall(r'\b\[\d+\]\b', text)

def verify_sources(output_text: str) -> tuple:
    """
    Verifies that cited sources have been visited.
    
    1. Finds all citations in the text.
    2. If citations are found, checks if browser history contains academic sources.
    3. If not, it blocks the output.
    
    Returns:
        tuple: (passed: bool, message: str)
    """
    citations = find_citations_in_text(output_text)
    
    if not citations:
        # No citations, no verification needed
        return True, "No citations found. Verification not required."

    # If citations are present, we expect proof of research
    history = get_browser_history()
    academic_domains = ["scholar.google", "arxiv.org", "nature.com", "ieee.org", "acm.org", "annas-archive.org"]
    
    has_visited_academic_source = any(
        any(domain in url for url in history) for domain in academic_domains
    )
    
    if not has_visited_academic_source:
        error_message = (
            "**CRITICAL VIOLATION (P4): Unverified Citations!**\n\n" 
            "- **Error:** The output contains citations, but there is no evidence of visiting academic sources.\n" 
            "- **Reason:** This violates the Citation Integrity Protocol. You cannot cite sources you haven't verified.\n" 
            "- **Action:** TASK BLOCKED. You MUST perform actual research by visiting sources before citing them."
        )
        return False, error_message

    return True, "Citations found and academic sources were visited. Verification passed."

if __name__ == '__main__':
    # Example Usage
    
    # --- TEST CASE 1: Contains citations, but no research history (SHOULD FAIL) ---
    BROWSER_HISTORY_API["visited_urls"] = ["https://www.google.com"]
    test_output_1 = "This is a claim based on research [1]."
    passed, message = verify_sources(test_output_1)
    print(f"Test 1 Passed: {passed}")
    if not passed:
        print(message)
    
    print("\n---\n")
    
    # --- TEST CASE 2: Contains citations AND has research history (SHOULD PASS) ---
    BROWSER_HISTORY_API["visited_urls"] = ["https://scholar.google.com/some_paper"]
    test_output_2 = "This is another claim from a different paper [2]."
    passed, message = verify_sources(test_output_2)
    print(f"Test 2 Passed: {passed}")
    if passed:
        print(message)
        
    print("\n---\n")

    # --- TEST CASE 3: No citations (SHOULD PASS) ---
    test_output_3 = "This is a simple statement with no claims."
    passed, message = verify_sources(test_output_3)
    print(f"Test 3 Passed: {passed}")
    if passed:
        print(message)
