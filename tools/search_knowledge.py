import logging
#!/usr/bin/env python3
"""
Knowledge Search CLI Tool
Fast and easy access to AI University knowledge base
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.knowledge_index import KnowledgeIndexer


def print_help():
    """Print usage help"""
    print("""
Knowledge Search Tool
=====================

Usage:
  search_knowledge.py <query>              Search all documents
  search_knowledge.py -t <type> <query>    Search specific type
  search_knowledge.py -r                   Rebuild index
  search_knowledge.py -s                   Show statistics
  search_knowledge.py -h                   Show this help

Document Types:
  lesson   - AI University lessons
  project  - Project documentation
  doc      - General documentation
  core     - Core system files

Examples:
  search_knowledge.py "cost optimization"
  search_knowledge.py -t lesson "external research"
  search_knowledge.py -r
  search_knowledge.py -s

""")


def format_result(result: dict, index: int) -> str:
    """Format a search result for display"""
    output = []
    output.append(f"\n{index}. {result['title']}")
    output.append(f"   {'─' * 60}")
    output.append(f"   Type: {result['doc_type']} | Score: {result['score']:.2f}")
    output.append(f"   Path: {result['path']}")
    
    if result['tags']:
        output.append(f"   Tags: {', '.join(result['tags'])}")
    
    output.append(f"\n   {result['excerpt']}\n")
    
    return '\n'.join(output)


def search_command(query: str, doc_type: str = None, limit: int = 10):
    """Execute search command"""
    print(f"\n🔍 Searching for: '{query}'")
    if doc_type:
        print(f"   Filtering by type: {doc_type}")
    print("=" * 70)
    
    indexer = KnowledgeIndexer()
    results = indexer.search(query, doc_type=doc_type, limit=limit)
    
    if not results:
        print("\n❌ No results found.")
        print("\nTips:")
        print("  - Try different keywords")
        print("  - Use fuzzy matching (e.g., 'optimizaton~' for 'optimization')")
        print("  - Search without type filter")
        return
    
    print(f"\n✅ Found {len(results)} result(s)\n")
    
    for i, result in enumerate(results, 1):
        print(format_result(result, i))
    
    print("=" * 70)


def rebuild_command(force: bool = True):
    """Execute rebuild index command"""
    print("\n🔨 Rebuilding Knowledge Index...")
    print("=" * 70)
    print()
    
    indexer = KnowledgeIndexer()
    indexed, skipped = indexer.index_all(force=force)
    
    print()
    print("=" * 70)
    print("✅ Index rebuild complete!")
    print("=" * 70)
    
    stats_command()


def stats_command():
    """Execute statistics command"""
    print("\n📊 Knowledge Base Statistics")
    print("=" * 70)
    print()
    
    indexer = KnowledgeIndexer()
    stats = indexer.get_stats()
    
    print(f"Total Documents:  {stats['total_documents']}")
    print(f"Index Size:       {stats['index_size'] / 1024:.2f} KB")
    print(f"Last Updated:     {stats['last_updated']}")
    print()
    
    print("Documents by Type:")
    print("-" * 40)
    for doc_type, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
        if count > 0:
            bar = '█' * min(count, 50)
            print(f"  {doc_type:12s}: {count:3d}  {bar}")
    
    print()
    print("=" * 70)


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    args = sys.argv[1:]
    
    # Handle flags
    if args[0] == '-h' or args[0] == '--help':
        print_help()
        return
    
    if args[0] == '-r' or args[0] == '--rebuild':
        rebuild_command()
        return
    
    if args[0] == '-s' or args[0] == '--stats':
        stats_command()
        return
    
    # Handle type filter
    doc_type = None
    query_start = 0
    
    if args[0] == '-t' or args[0] == '--type':
        if len(args) < 3:
            print("❌ Error: -t requires document type and query")
            print_help()
            return
        doc_type = args[1]
        query_start = 2
    
    # Get query
    query = ' '.join(args[query_start:])
    
    if not query:
        print("❌ Error: No search query provided")
        print_help()
        return
    
    # Execute search
    search_command(query, doc_type=doc_type)


if __name__ == '__main__':
    main()
