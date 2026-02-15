# Manus Global Knowledge - Master Index

**Last Updated:** 2026-02-14  
**Purpose:** Central index of ALL knowledge across ALL projects for cross-project access

---

## Projects Registry

### Active Projects

| Project | Profile | Status | Last Updated |
|---------|---------|--------|--------------|
| IntellTech | `/projects/intelltech/PROJECT_PROFILE.md` | Active | 2026-02-14 |

### How to Add New Project

1. Create `/projects/{project_name}/` directory
2. Add `PROJECT_PROFILE.md` with project overview
3. Update this MASTER_INDEX
4. Run search index rebuild

---

## Cross-Project Entities

### Companies (Total: 150+)

**By Sector:**
- Mining: 50+ companies (IntellTech)
- Construction: 30+ companies (IntellTech)
- Infrastructure: 20+ companies (IntellTech)
- Oil & Gas: 15+ companies (IntellTech)
- Railways: 10+ companies (IntellTech)

**By Country:**
- Australia: 40+ companies (IntellTech)
- India: 30+ companies (IntellTech)
- Indonesia: 20+ companies (IntellTech)
- Malaysia: 15+ companies (IntellTech)
- Singapore: 10+ companies (IntellTech)
- Other APAC: 35+ companies (IntellTech)

**Location:** `/projects/intelltech/data/`

### Contacts (Total: 200+)

- C-Level Executives: 50+ (IntellTech)
- Engineering Managers: 80+ (IntellTech)
- Procurement: 40+ (IntellTech)
- Operations: 30+ (IntellTech)

**Location:** `/projects/intelltech/data/`

### Technologies & Products

- SHMS (Structural Health Monitoring System) - IntellTech
- Geo Inspector - IntellTech
- Geotechnical Monitoring - IntellTech

---

## Knowledge Areas (Cross-Project)

### Market Intelligence

| Topic | Location | Projects |
|-------|----------|----------|
| APAC Infrastructure Investment | `/projects/intelltech/data/APAC_infrastructure_investment.md` | IntellTech |
| SHM Market Data | `/projects/intelltech/data/SHM_market_intelligence.md` | IntellTech |
| Competitive Intelligence | `/projects/intelltech/data/competitive_intelligence.md` | IntellTech |

### Processes & SOPs

| Process | Location | Applicable To |
|---------|----------|---------------|
| Lead Generation | `/cross_project/lead_generation_process.md` | All Projects |
| Market Research | `/cross_project/market_research_process.md` | All Projects |
| Report Writing | `/cross_project/report_writing_process.md` | All Projects |

### Case Studies

| Case Study | Sector | Country | Location |
|------------|--------|---------|----------|
| MRT Tunnelling Singapore | Construction | Singapore | `/projects/intelltech/data/case_studies/construction_mrt_singapore.md` |
| Cadia Mine Australia | Mining | Australia | `/projects/intelltech/data/case_studies/mining_cadia_australia.md` |
| Donghai Wind Farm China | Energy | China | `/projects/intelltech/data/case_studies/energy_donghai_china.md` |
| (8 more case studies) | Various | Various | `/projects/intelltech/data/case_studies/` |

---

## Search Index (Fast Lookup)

### By Entity Type

- **Companies:** `/search_index/companies.json`
- **Contacts:** `/search_index/contacts.json`
- **Countries:** `/search_index/countries.json`
- **Sectors:** `/search_index/sectors.json`
- **Technologies:** `/search_index/technologies.json`

### By Keyword

- **"mining"** → 50+ companies, 3 case studies, 1 market report
- **"australia"** → 40+ companies, 2 case studies, 1 country analysis
- **"shms"** → IntellTech product, 11 sectors, 10 case studies
- **"tailings dam"** → Cadia case study, GISTM framework, mining sector
- **"bridge monitoring"** → Penang case study, infrastructure sector

### Full-Text Search

**Location:** `/search_index/full_text_index.json`

**Usage:**
```bash
# Search for any term across all knowledge
grep -r "search_term" /home/ubuntu/manus_global_knowledge/
```

---

## Cross-References

### IntellTech ↔ Other Projects

*To be populated as new projects are added*

### Shared Contacts

*To be populated when contacts appear in multiple projects*

### Shared Companies

*To be populated when companies appear in multiple projects*

---

## Quick Access Commands

### For Agent Use

```markdown
# Load all project profiles
READ /home/ubuntu/manus_global_knowledge/projects/*/PROJECT_PROFILE.md

# Search for company
SEARCH /home/ubuntu/manus_global_knowledge/ FOR "company_name"

# List all companies in sector
READ /home/ubuntu/manus_global_knowledge/search_index/sectors/{sector_name}.json

# Cross-project entity lookup
READ /home/ubuntu/manus_global_knowledge/cross_project/shared_entities.md
```

### For User Commands

- `@search [term]` → Full-text search across all projects
- `@projects` → List all available projects
- `@cross [entity]` → Show where entity appears across projects
- `@index` → Display this master index

---

## Sync Status

**Google Drive Backup:** `manus_google_drive:Manus_Knowledge/`  
**Last Sync:** 2026-02-14  
**Auto-Sync:** Enabled (after each knowledge update)

---

## Statistics

- **Total Projects:** 1
- **Total Companies:** 150+
- **Total Contacts:** 200+
- **Total Case Studies:** 10
- **Total Market Reports:** 3
- **Total Size:** 5.6 MB

---

**This index is automatically updated when new knowledge is added to any project.**
