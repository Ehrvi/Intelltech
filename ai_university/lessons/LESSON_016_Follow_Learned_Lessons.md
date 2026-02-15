# Lesson 016: MUST Follow Learned Lessons

**Domain:** Quality Assurance  
**Created:** 2026-02-13  
**Source:** IntellTech Project - Sandbox Reset Failure

---

## The Problem

**What happened:**
- Created Lesson 015 (Sandbox Storage is Temporary)
- Immediately violated it by not backing up Stage 1 results
- Sandbox reset → All progress lost
- Had to restart from scratch

**Root cause:** Creating lessons but not APPLYING them

---

## The Solution

### Golden Rule
**"Lessons exist to be FOLLOWED, not just documented"**

### Implementation Checklist

Before EVERY action, ask:
1. ✅ Is there a relevant lesson in AI University?
2. ✅ Am I following that lesson RIGHT NOW?
3. ✅ If not, STOP and follow it first

### Specific Applications

**Lesson 015 (Sandbox Backup):**
- Create file → IMMEDIATELY backup to Google Drive
- Don't wait, don't batch, don't "do it later"
- Command: `rclone copy <file> manus_google_drive:IntellTech/Data/`

**Lesson 001 (Prompt Optimization):**
- Before using any prompt → Check if it preserves critical details
- Apply checklist BEFORE execution

**Lesson 014 (API Error Handling):**
- Before any API call → Implement retry logic
- Don't assume it will work

---

## Validation Checklist

Before marking task complete:
- [ ] All relevant lessons identified
- [ ] All lessons applied during execution
- [ ] New lesson created if new pattern discovered
- [ ] All outputs backed up to Google Drive

---

## Example: This Task

**Lessons that should have been followed:**
1. ✅ Lesson 015: Backup Stage 1 results immediately
2. ✅ Lesson 014: Apollo retry handler
3. ✅ Lesson 001: Prompt v13 optimization

**What actually happened:**
1. ❌ Stage 1 completed but NOT backed up
2. ✅ Apollo retry handler used
3. ✅ Prompt v13 referenced

**Result:** 33% lesson compliance → Failure

---

## Success Criteria

**100% lesson compliance** = All relevant lessons applied

**Anything less** = Risk of failure

---

## Meta-Lesson

**This lesson itself must be followed:**
- Before every task → Review AI University
- During every task → Apply relevant lessons
- After every task → Create new lessons if needed

**Recursive enforcement:** Following this lesson ensures all other lessons are followed.

---

**Status:** Active  
**Priority:** CRITICAL  
**Enforcement:** Mandatory for all tasks
