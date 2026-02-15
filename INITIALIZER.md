# Manus Global Knowledge - INITIALIZER

**Version:** 3.0 Global Cross-Project  
**Last Updated:** 2026-02-14  
**Purpose:** Auto-initialize Manus agent with FULL cross-project knowledge access

---

## 🚀 MANDATORY INITIALIZATION SEQUENCE

This runs at the start of EVERY Manus conversation, providing unlimited cross-project knowledge access at zero cost.

---

### Step 0: Sync from GitHub (MANDATORY FIRST)

**Purpose:** Ensure you always have the latest version of the knowledge system.

```bash
# Clone if doesn't exist, pull if exists
if [ ! -d /home/ubuntu/manus_global_knowledge ]; then
  git clone https://github.com/Ehrvi/Intelltech.git /home/ubuntu/manus_global_knowledge
fi

cd /home/ubuntu/manus_global_knowledge && git pull origin main
```

---

### Step 1: Credit Check (MANDATORY)

**Purpose:** Ensure APIs have credits before routing tasks.

```bash
# Check all API credits (MANDATORY)
python3.11 /home/ubuntu/skills/ai-task-optimizer/scripts/credit_monitor.py
```

**Actions:**
- ✅ All APIs healthy → Proceed
- ⚠️ Low credits → Notify user, proceed
- 🚨 No credits → Notify user urgently, fallback to Manus-only

---

### Step 2: Optimized Knowledge Sync (Phase 1 - Cache-First)

**Purpose:** Get latest knowledge with 80-90% credit savings.

```bash
# Log conversation start (for metrics)
python3 /home/ubuntu/manus_global_knowledge/metrics/collect_metrics.py conversation_start

# Optimized sync (cache-first strategy)
cd /home/ubuntu/manus_global_knowledge && ./optimized_sync.sh pull
```

**How it works:**
- ✅ Cache fresh (<24h) → Use local, ZERO Drive calls
- ⚠️ Cache stale (>24h) → Sync from Drive once
- 📊 Automatic metrics collection

**Expected savings:** 80-90% credit reduction

---

### Step 3: Load Master Index (ALL Projects)

**ALWAYS load:**

```
READ /home/ubuntu/manus_global_knowledge/MASTER_INDEX.md
```

This provides:

**CRITICAL - Scientific Methodology Requirements:**

```
READ /home/ubuntu/manus_global_knowledge/core/SCIENTIFIC_METHODOLOGY_REQUIREMENTS.md
```

**All subsequent responses MUST comply with scientific methodology standards:**
- Evidence-based claims with citations
- Methodological transparency
- Quantitative analysis
- Comparative evaluation
- Limitations disclosure
- Registry of ALL projects
- Cross-project entity index (companies, contacts, technologies)
- Knowledge areas map
- Search index locations

---

### Step 4: Load Core Universal Frameworks

**ALWAYS load these files (universal for all projects):**

1. `/home/ubuntu/manus_university/core/DECISION_TREE.md`
   - Tool selection framework (Manus vs GPT vs APIs)

2. `/home/ubuntu/manus_university/core/COST_OPTIMIZATION.md`
   - 3-tier cost model for all tasks

3. `/home/ubuntu/manus_university/core/QUALITY_STANDARDS.md`
   - Quality thresholds and validation criteria

4. `/home/ubuntu/manus_university/core/LESSONS_LEARNED.md`
   - Universal lessons applicable to all projects

---

### Step 5: Detect Current Project Context (if any)

```
IF project_context exists in user message or conversation:
    project_name = extract_project_name()
    project_path = /home/ubuntu/manus_global_knowledge/projects/{project_name}/
    
    IF project_path exists:
        READ {project_path}/PROJECT_PROFILE.md
        LOG: "Project context: {project_name}"
    ELSE:
        LOG: "Project {project_name} not found in global knowledge"
        CREATE new project structure
ELSE:
    project_name = "general"
    LOG: "No specific project context detected"
```

---

### Step 6: Enable Cross-Project Search

**Set global search mode:**

```
global_search_enabled = TRUE
search_index_loaded = TRUE
cross_project_access = UNLIMITED
```

**Available search commands:**
- `@search [term]` → Full-text search across ALL projects
- `@projects` → List all available projects
- `@cross [entity]` → Show where entity appears across projects
- `@index` → Display master index

---

### Step 7: Apply Unified Routing Logic

**Integrated decision system combining:**
- First Rule Over All (OpenAI capable?)
- AI Task Optimizer (route to OpenAI/API/Manus)
- Architecture Selector (Guardian/Parallel/Hybrid)
- Guardian validation (quality assurance)

**Routing Flow:**

```
User Task
    ↓
[Quick Check] First Rule: Can OpenAI do this?
    ├─→ NO → Direct Manus (strategic/critical)
    └─→ YES → Continue
    ↓
[Task Analysis] AI Task Optimizer: Route where?
    ├─→ Specialized API (Apollo, Gmail, etc.)
    ├─→ OpenAI (90% of tasks)
    └─→ Manus (10% critical)
    ↓
[If using workers] Architecture Selector: Which architecture?
    ├─→ Guardian (bulk/research)
    ├─→ Parallel Map (homogeneous items)
    ├─→ Hybrid (multi-stage)
    └─→ Direct Manus (override)
    ↓
[Execute]
    ↓
[Validate] Guardian middleware (if applicable)
    ├─→ Quality ≥ 80 → Deliver
    └─→ Quality < 80 → Escalate to Manus
```

**Decision Factors:**

1. **Complexity:** 1-10 (10 = highest)
2. **Volume:** Number of items to process
3. **Criticality:** 1-10 (10 = mission critical)
4. **Homogeneity:** 1-10 (10 = identical subtasks)
5. **Client-facing:** Yes | No
6. **Strategic:** Yes | No

**Log Decision:**
- Tool selected: [OpenAI | Manus | API | Guardian | Parallel]
- Reason: [brief justification]
- Expected cost: [$X.XX | Y credits]
- Project context: [{project_name} | cross-project]

---

### Step 8: Execute with Cost Optimization & Cross-Project Access

1. **Check for reusable assets (across ALL projects):**
   - Templates in `/manus_university/templates/`
   - Processes in `/manus_global_knowledge/cross_project/`
   - Data in any `/projects/*/data/`

2. **Apply cost-saving strategies:**
   - Batch processing
   - Caching
   - Incremental updates
   - Parallel processing (when appropriate)
   - **Cross-project data reuse** (NEW!)

3. **Validate quality:**
   - Use thresholds from QUALITY_STANDARDS.md
   - Escalate to Manus if quality < threshold

---

### Step 9: Cross-Project Entity Lookup (Automatic)

**When any entity is mentioned:**

```
entity_type = detect_entity_type(mention)  # company, contact, technology, etc.

IF entity_type:
    # Search across ALL projects
    results = search_global_knowledge(entity_name)
    
    IF results found in multiple projects:
        LOG: "{entity_name} appears in {count} projects"
        SHOW cross-references to user (if relevant)
```

**Example:**
- User mentions "BHP Group" in IntellTech conversation
- System finds: IntellTech (lead), Project B (client), Project C (competitor analysis)
- Agent can pull data from all 3 projects seamlessly

---

### Step 10: Post-Task Learning & Sync

After completing ANY task:

1. **Update lessons learned:**
   - If universal lesson → `/manus_university/core/LESSONS_LEARNED.md`
   - If project-specific → `{project_path}/LESSONS_LEARNED.md`

2. **Update search indices:**
   ```bash
   python3 /home/ubuntu/manus_global_knowledge/build_search_index.py
   ```

3. **Sync to Google Drive (zero cost):**
   ```bash
   rclone sync /home/ubuntu/manus_global_knowledge/ \
     manus_google_drive:Manus_Knowledge/ \
     --config /home/ubuntu/.gdrive-rclone.ini
   ```

4. **Archive completed work:**
   - Move to `/projects/{project_name}/archives/{date}_{task}/`

---

## 📊 Decision Matrix Quick Reference

| Task Type | Complexity | Criticality | Tool | Cost Tier |
|-----------|------------|-------------|------|-----------|
| Research | Simple | Low | GPT-4o-mini | 1 |
| Analysis | Moderate | Medium | GPT-4o | 2 |
| Strategy | Complex | High | GPT-4o + Manus validation | 2+3 |
| Client deliverable | Any | Critical | Manus | 3 |
| Cross-project search | Any | Any | Local (zero cost) | 0 |

---

## 🎯 Universal Principles (Apply to ALL Projects)

1. **Cost-First Mindset:** Always choose the cheapest option that meets quality requirements
2. **Quality-Aware:** Know when to escalate to premium tools
3. **Single Source of Truth:** All knowledge consolidated in global system
4. **Continuous Learning:** Every task adds to the knowledge base
5. **Modular & Reusable:** Processes and templates work across projects
6. **Cross-Project Access:** UNLIMITED access to all project knowledge (NEW!)
7. **Zero Additional Costs:** All cross-project access is local (NEW!)

---

## 🔄 Multi-Project Architecture with Cross-References

```
/manus_global_knowledge/
├── MASTER_INDEX.md              # Central index of ALL knowledge
├── INITIALIZER.md               # This file
├── projects/                    # All projects
│   ├── intelltech/
│   ├── project_b/
│   └── project_c/
├── cross_project/               # Shared knowledge
│   └── shared_processes.md
└── search_index/                # Fast lookup (zero cost)
    ├── companies.json
    ├── contacts.json
    ├── countries.json
    ├── sectors.json
    └── full_text_index.json
```

---

## ✅ Initialization Checklist

Before proceeding with user's request:

- [ ] Global knowledge synced from Google Drive
- [ ] Master index loaded (ALL projects accessible)
- [ ] Core frameworks loaded (DECISION_TREE, COST_OPTIMIZATION, QUALITY_STANDARDS)
- [ ] Project context detected (or set to "general")
- [ ] Project-specific knowledge loaded (if applicable)
- [ ] Cross-project search enabled
- [ ] Decision tree applied to current task
- [ ] Tool selected and justified
- [ ] Cost optimization strategies identified
- [ ] Ready to execute with FULL cross-project knowledge access

---

## 🚨 Critical Rules

1. **NEVER skip Step 0 (sync)** - Ensures latest knowledge from all conversations
2. **ALWAYS enable cross-project search** - Core feature of this system
3. **ALWAYS log tool selection** - For cost tracking
4. **ALWAYS validate quality** - Before delivering
5. **ALWAYS update lessons** - After completing
6. **ALWAYS sync back to Google Drive** - After any knowledge update
7. **ALWAYS optimize costs** - Default to lower tiers

---

**Initialization complete. Proceed with user's request using selected tool, cost optimization strategies, and FULL cross-project knowledge access.**
