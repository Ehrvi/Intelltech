import logging
"""
Modern Knowledge Indexing System
Fast, reliable, and scalable indexing for AI University knowledge base
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re

from whoosh.fields import Schema, TEXT, ID, DATETIME, KEYWORD
from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import QueryParser, MultifieldParser, FuzzyTermPlugin
from whoosh.query import And, Or, Term
from whoosh import scoring


class KnowledgeIndexer:
    """
    Modern file indexing system for exponentially growing knowledge base.
    
    Features:
    - Full-text search (< 100ms)
    - Incremental indexing
    - Fuzzy matching
    - Relevance ranking
    - Cross-references
    - Metadata filtering
    """
    
    def __init__(self, base_path: str = None):
        """Initialize the indexer"""
        if base_path is None:
            base_path = Path(__file__).parent.parent
        
        self.base_path = Path(base_path)
        self.index_dir = self.base_path / "search_index"
        self.cache_file = self.base_path / "search_index" / "file_cache.json"
        
        # Define schema
        self.schema = Schema(
            path=ID(stored=True, unique=True),
            filename=TEXT(stored=True),
            title=TEXT(stored=True, field_boost=2.0),
            content=TEXT(stored=True),
            tags=KEYWORD(stored=True, commas=True, scorable=True),
            doc_type=ID(stored=True),  # lesson, project, doc, core
            created=DATETIME(stored=True),
            modified=DATETIME(stored=True),
            author=TEXT(stored=True),
            references=KEYWORD(stored=True, commas=True)
        )
        
        # Initialize index
        self._init_index()
        
        # Load file cache
        self.file_cache = self._load_cache()
    
    def _init_index(self):
        """Initialize or open the search index"""
        if not self.index_dir.exists():
            self.index_dir.mkdir(parents=True)
        
        if exists_in(str(self.index_dir)):
            self.index = open_dir(str(self.index_dir))
        else:
            self.index = create_in(str(self.index_dir), self.schema)
    
    def _load_cache(self) -> Dict:
        """Load file hash cache for incremental indexing"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        """Save file hash cache"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.file_cache, f, indent=2)
    
    def _file_hash(self, filepath: Path) -> str:
        """Calculate file hash for change detection"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _extract_metadata(self, content: str, filepath: Path) -> Dict:
        """Extract metadata from markdown file"""
        metadata = {
            'title': filepath.stem.replace('_', ' '),
            'tags': [],
            'author': '',
            'created': None,
            'references': []
        }
        
        # Extract title from first # heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # Extract tags (look for **Tags:** or **Domain:** lines)
        tags_match = re.search(r'\*\*(?:Tags|Domain):\*\*\s+(.+)$', content, re.MULTILINE)
        if tags_match:
            tags_str = tags_match.group(1).strip()
            metadata['tags'] = [t.strip() for t in tags_str.split(',')]
        
        # Extract author
        author_match = re.search(r'\*\*Author:\*\*\s+(.+)$', content, re.MULTILINE)
        if author_match:
            metadata['author'] = author_match.group(1).strip()
        
        # Extract created date
        created_match = re.search(r'\*\*Created:\*\*\s+(.+)$', content, re.MULTILINE)
        if created_match:
            try:
                date_str = created_match.group(1).strip()
                metadata['created'] = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                pass
        
        # Extract references (markdown links)
        references = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        metadata['references'] = [ref[1] for ref in references if ref[1].endswith('.md')]
        
        return metadata
    
    def _determine_doc_type(self, filepath: Path) -> str:
        """Determine document type from path"""
        path_str = str(filepath.relative_to(self.base_path))
        
        if 'ai_university/lessons' in path_str:
            return 'lesson'
        elif 'projects/' in path_str:
            return 'project'
        elif 'core/' in path_str:
            return 'core'
        elif 'docs/' in path_str:
            return 'doc'
        else:
            return 'other'
    
    def index_file(self, filepath: Path) -> bool:
        """Index a single file"""
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            metadata = self._extract_metadata(content, filepath)
            
            # Get file stats
            stats = filepath.stat()
            modified = datetime.fromtimestamp(stats.st_mtime)
            created = metadata['created'] or datetime.fromtimestamp(stats.st_ctime)
            
            # Determine document type
            doc_type = self._determine_doc_type(filepath)
            
            # Index document
            writer = self.index.writer()
            writer.update_document(
                path=str(filepath.relative_to(self.base_path)),
                filename=filepath.name,
                title=metadata['title'],
                content=content,
                tags=','.join(metadata['tags']),
                doc_type=doc_type,
                created=created,
                modified=modified,
                author=metadata['author'],
                references=','.join(metadata['references'])
            )
            writer.commit()
            
            return True
            
        except Exception as e:
            print(f"Error indexing {filepath}: {e}")
            return False
    
    def index_all(self, force: bool = False) -> Tuple[int, int]:
        """
        Index all markdown files in the knowledge base.
        
        Args:
            force: If True, re-index all files regardless of cache
        
        Returns:
            Tuple of (indexed_count, skipped_count)
        """
        indexed = 0
        skipped = 0
        
        # Find all markdown files
        md_files = list(self.base_path.rglob('*.md'))
        
        print(f"📚 Found {len(md_files)} markdown files")
        print()
        
        for filepath in md_files:
            # Skip files in search_index directory
            if 'search_index' in str(filepath):
                continue
            
            # Check if file needs indexing
            file_hash = self._file_hash(filepath)
            cache_key = str(filepath.relative_to(self.base_path))
            
            if not force and cache_key in self.file_cache:
                if self.file_cache[cache_key] == file_hash:
                    skipped += 1
                    continue
            
            # Index file
            if self.index_file(filepath):
                self.file_cache[cache_key] = file_hash
                indexed += 1
                print(f"✓ Indexed: {filepath.name}")
        
        # Save cache
        self._save_cache()
        
        print()
        print(f"✅ Indexing complete: {indexed} indexed, {skipped} skipped")
        
        return indexed, skipped
    
    def search(self, 
               query_str: str, 
               doc_type: Optional[str] = None,
               tags: Optional[List[str]] = None,
               limit: int = 20) -> List[Dict]:
        """
        Search the knowledge base.
        
        Args:
            query_str: Search query
            doc_type: Filter by document type (lesson, project, doc, core)
            tags: Filter by tags
            limit: Maximum results to return
        
        Returns:
            List of search results with metadata
        """
        results = []
        
        with self.index.searcher(weighting=scoring.BM25F()) as searcher:
            # Create query parser with fuzzy matching
            parser = MultifieldParser(
                ['title', 'content', 'tags', 'filename'],
                schema=self.index.schema
            )
            parser.add_plugin(FuzzyTermPlugin())
            
            # Parse query
            query = parser.parse(query_str)
            
            # Add filters
            filters = []
            if doc_type:
                filters.append(Term('doc_type', doc_type))
            if tags:
                for tag in tags:
                    filters.append(Term('tags', tag))
            
            if filters:
                query = And([query] + filters)
            
            # Execute search
            search_results = searcher.search(query, limit=limit)
            
            # Format results
            for hit in search_results:
                results.append({
                    'path': hit['path'],
                    'filename': hit['filename'],
                    'title': hit['title'],
                    'doc_type': hit['doc_type'],
                    'tags': hit['tags'].split(',') if hit['tags'] else [],
                    'score': hit.score,
                    'excerpt': self._get_excerpt(hit['content'], query_str)
                })
        
        return results
    
    def _get_excerpt(self, content: str, query: str, context: int = 100) -> str:
        """Get relevant excerpt from content"""
        # Find first occurrence of query term
        query_terms = query.lower().split()
        content_lower = content.lower()
        
        for term in query_terms:
            pos = content_lower.find(term)
            if pos != -1:
                start = max(0, pos - context)
                end = min(len(content), pos + len(term) + context)
                excerpt = content[start:end]
                
                # Clean up
                if start > 0:
                    excerpt = '...' + excerpt
                if end < len(content):
                    excerpt = excerpt + '...'
                
                return excerpt.strip()
        
        # No match, return first 200 chars
        return content[:200] + '...' if len(content) > 200 else content
    
    def find_related(self, filepath: str, limit: int = 5) -> List[Dict]:
        """Find documents related to the given file"""
        with self.index.searcher() as searcher:
            # Get document
            doc = searcher.document(path=filepath)
            if not doc:
                return []
            
            # Search by tags
            if doc['tags']:
                tags = doc['tags'].split(',')
                tag_query = ' OR '.join([f'tags:{tag}' for tag in tags])
                
                parser = QueryParser('tags', self.index.schema)
                query = parser.parse(tag_query)
                
                results = searcher.search(query, limit=limit + 1)
                
                related = []
                for hit in results:
                    if hit['path'] != filepath:  # Exclude self
                        related.append({
                            'path': hit['path'],
                            'title': hit['title'],
                            'doc_type': hit['doc_type'],
                            'score': hit.score
                        })
                
                return related[:limit]
        
        return []
    
    def get_stats(self) -> Dict:
        """Get indexing statistics"""
        with self.index.searcher() as searcher:
            total_docs = searcher.doc_count_all()
            
            # Count by type
            type_counts = {}
            for doc_type in ['lesson', 'project', 'doc', 'core', 'other']:
                query = Term('doc_type', doc_type)
                results = searcher.search(query, limit=None)
                type_counts[doc_type] = len(results)
            
            return {
                'total_documents': total_docs,
                'by_type': type_counts,
                'index_size': sum(f.stat().st_size for f in self.index_dir.glob('*')),
                'last_updated': datetime.now().isoformat()
            }


def rebuild_index(force: bool = False):
    """Rebuild the entire knowledge index"""
    print("🔨 Building Knowledge Index...")
    print("=" * 70)
    print()
    
    indexer = KnowledgeIndexer()
    indexed, skipped = indexer.index_all(force=force)
    
    print()
    print("=" * 70)
    print("📊 INDEX STATISTICS")
    print("=" * 70)
    
    stats = indexer.get_stats()
    print(f"Total Documents: {stats['total_documents']}")
    print(f"Index Size: {stats['index_size'] / 1024:.2f} KB")
    print()
    print("By Type:")
    for doc_type, count in stats['by_type'].items():
        if count > 0:
            print(f"  {doc_type:12s}: {count:3d}")
    print()
    
    return indexer


def search_knowledge(query: str, doc_type: str = None, limit: int = 10):
    """Search the knowledge base"""
    indexer = KnowledgeIndexer()
    results = indexer.search(query, doc_type=doc_type, limit=limit)
    
    print(f"🔍 Search Results for: '{query}'")
    print("=" * 70)
    print()
    
    if not results:
        print("No results found.")
        return
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   Type: {result['doc_type']} | Score: {result['score']:.2f}")
        print(f"   Path: {result['path']}")
        if result['tags']:
            print(f"   Tags: {', '.join(result['tags'])}")
        print(f"   {result['excerpt']}")
        print()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'rebuild':
            rebuild_index(force=True)
        elif sys.argv[1] == 'search':
            if len(sys.argv) > 2:
                search_knowledge(' '.join(sys.argv[2:]))
            else:
                print("Usage: python knowledge_index.py search <query>")
        elif sys.argv[1] == 'stats':
            indexer = KnowledgeIndexer()
            stats = indexer.get_stats()
            print(json.dumps(stats, indent=2))
    else:
        rebuild_index()
