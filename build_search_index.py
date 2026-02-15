#!/usr/bin/env python3
"""
Build search indices for Manus Global Knowledge
Zero-cost local search across all projects
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Base path
BASE_PATH = Path("/home/ubuntu/manus_global_knowledge")
PROJECTS_PATH = BASE_PATH / "projects"
SEARCH_INDEX_PATH = BASE_PATH / "search_index"

def build_indices():
    """Build all search indices"""
    
    # Initialize indices
    companies = []
    contacts = []
    countries = defaultdict(list)
    sectors = defaultdict(list)
    technologies = []
    full_text = {}
    
    # Scan all projects
    for project_dir in PROJECTS_PATH.iterdir():
        if not project_dir.is_dir():
            continue
            
        project_name = project_dir.name
        print(f"Indexing project: {project_name}")
        
        # Index all markdown files
        for md_file in project_dir.rglob("*.md"):
            rel_path = str(md_file.relative_to(BASE_PATH))
            
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # Add to full-text index
                full_text[rel_path] = {
                    "path": rel_path,
                    "project": project_name,
                    "size": len(content),
                    "preview": content[:200]
                }
                
                # Extract entities (simple keyword matching)
                content_lower = content.lower()
                
                # Countries
                country_keywords = ['australia', 'india', 'indonesia', 'malaysia', 
                                  'singapore', 'thailand', 'vietnam', 'philippines',
                                  'south korea', 'japan', 'new zealand', 'china']
                for country in country_keywords:
                    if country in content_lower:
                        countries[country].append({
                            "file": rel_path,
                            "project": project_name
                        })
                
                # Sectors
                sector_keywords = ['mining', 'construction', 'infrastructure', 
                                 'oil & gas', 'railways', 'water', 'dams',
                                 'environmental', 'renewable energy', 'ports',
                                 'maritime', 'energy']
                for sector in sector_keywords:
                    if sector in content_lower:
                        sectors[sector].append({
                            "file": rel_path,
                            "project": project_name
                        })
                
                # Technologies
                tech_keywords = ['shms', 'geo inspector', 'structural health monitoring',
                               'geotechnical monitoring', 'iot', 'sensors']
                for tech in tech_keywords:
                    if tech in content_lower:
                        if tech not in [t['name'] for t in technologies]:
                            technologies.append({
                                "name": tech,
                                "projects": [project_name],
                                "files": [rel_path]
                            })
                        else:
                            for t in technologies:
                                if t['name'] == tech:
                                    if project_name not in t['projects']:
                                        t['projects'].append(project_name)
                                    if rel_path not in t['files']:
                                        t['files'].append(rel_path)
                
            except Exception as e:
                print(f"Error indexing {md_file}: {e}")
                continue
    
    # Write indices to JSON files
    SEARCH_INDEX_PATH.mkdir(exist_ok=True)
    
    (SEARCH_INDEX_PATH / "countries.json").write_text(
        json.dumps(dict(countries), indent=2)
    )
    
    (SEARCH_INDEX_PATH / "sectors.json").write_text(
        json.dumps(dict(sectors), indent=2)
    )
    
    (SEARCH_INDEX_PATH / "technologies.json").write_text(
        json.dumps(technologies, indent=2)
    )
    
    (SEARCH_INDEX_PATH / "full_text_index.json").write_text(
        json.dumps(full_text, indent=2)
    )
    
    # Write summary
    summary = {
        "last_updated": "2026-02-14",
        "total_files": len(full_text),
        "total_countries": len(countries),
        "total_sectors": len(sectors),
        "total_technologies": len(technologies)
    }
    
    (SEARCH_INDEX_PATH / "summary.json").write_text(
        json.dumps(summary, indent=2)
    )
    
    print("\n✅ Search indices built successfully!")
    print(f"- Files indexed: {len(full_text)}")
    print(f"- Countries: {len(countries)}")
    print(f"- Sectors: {len(sectors)}")
    print(f"- Technologies: {len(technologies)}")

if __name__ == "__main__":
    build_indices()
