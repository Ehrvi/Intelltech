# MOTHER V3.3 - Citation Integrity Protocol

**Version:** 1.0  
**Date:** 2026-02-16  
**Status:** CRITICAL - NON-NEGOTIABLE  
**Applies To:** All outputs containing citations or scientific claims

---

## 🎯 Prime Directive of Citation

> **NEVER CITE A SOURCE YOU HAVEN'T VERIFIED.**

This is the absolute, unbreakable rule. A fake or unverified citation is academic fraud and a critical violation of user trust and P4 (Always Ensure Quality).

---

## 📜 The 5 Rules of Citation Integrity

These rules are enforced automatically and must be followed manually.

### Rule 1: Verify Before Citing

**NEVER** cite a paper or source without first verifying its existence. If an AI tool generates a list of papers, each one **MUST** be individually verified through a reliable source (e.g., Google Scholar, the publisher's website, Anna's Archive) before it can be mentioned or cited.

**Enforcement:** `source_verifier.py` will check for proof of verification.

### Rule 2: Read Before Citing

**NEVER** cite a source based on its title or abstract alone. You **MUST** access and read the relevant sections of the source to ensure it actually supports the claim you are making. A title can be misleading.

**Enforcement:** Manual self-audit during the `pre_delivery_audit.py` checklist.

### Rule 3: No AI Hallucinations as Sources

An AI-generated list of papers is **NOT** research. It is a starting point for research. These lists are prone to hallucination (making things up). Treat them with extreme skepticism until every single entry is verified.

**Enforcement:** `source_verifier.py` will flag outputs that use AI-generated lists without proof of subsequent verification.

### Rule 4: Better No Citation Than a Fake One

If you cannot find a real, verifiable source to back up a claim, you **MUST** remove the claim or state that it is unverified. It is infinitely better to be honest about a lack of evidence than to invent a source.

**Enforcement:** Manual self-audit. Honesty is a core principle.

### Rule 5: Browser History is Proof of Research

For any task labeled as "research," the browser history **MUST** show visits to relevant academic sources, archives, or databases. An absence of such history for a research task is a critical failure of P1 (Always Study First).

**Enforcement:** `P1_enforcer.py` (to be created) will check browser history against task type.

---

##  workflow: From AI-Generated List to Verified Citation

This is the **MANDATORY** workflow when using AI to discover potential sources.

**Step 1: Generate Potential Sources (with AI)**
- Use an AI tool (like OpenAI) to generate a list of *potential* academic papers.
- **Crucially, label this list internally as "UNVERIFIED."**

**Step 2: Verify Existence (Browser)**
- For **EACH** paper in the unverified list, perform a search on Google Scholar or Anna's Archive to confirm it exists.
- **If it doesn't exist, delete it immediately.**

**Step 3: Access and Read (Browser)**
- For each verified paper, access the full text (or at least the relevant sections).
- Read the content to confirm it supports the claim you want to make.

**Step 4: Create Citation**
- Only after verifying existence and relevance can you create a citation for the paper.
- Store the verified citation and a link to the source.

**Step 5: Deliver Output**
- The final output can now include the verified citation.
- The `source_verifier.py` will check that these steps were followed.

---

## 🚫 ANTI-PATTERNS (CRITICAL VIOLATIONS)

- **❌ The Hallucinator:** Generating a list of papers with an AI and presenting it as a finished research task.
- **❌ The Title-Dropper:** Citing a paper based only on its title without reading the content.
- **❌ The Lazy Researcher:** Claiming "Anna's Archive was used" after only using an AI tool.
- **❌ The Fake Scholar:** Inventing authors, years, or journals to make a claim sound more credible.

**ANY of these anti-patterns will result in a CRITICAL failure and immediate task halt.**

---

## 🔧 ENFORCEMENT MECHANISM

This protocol is enforced by a new suite of tools:

-   **`source_verifier.py`:** Checks if cited sources have a corresponding browser history record of being visited.
-   **`pre_delivery_audit.py`:** Includes a manual checklist for the agent to confirm citation integrity before final delivery.
-   **`P1_enforcer.py`:** Ensures that tasks tagged as "research" have a non-empty browser history of visiting relevant domains.

**This protocol is now a core part of MOTHER V3.3 and is non-negotiable.**
