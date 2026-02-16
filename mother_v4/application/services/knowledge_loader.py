"""
Knowledge Loader - Composite Pattern Implementation

Loads and manages knowledge hierarchy (principles, documents, sources).

Pattern: Composite (Gang of Four, 1994)
Purpose: Treat individual objects and compositions uniformly
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class KnowledgeType(Enum):
    """Types of knowledge components"""
    PRINCIPLE = "principle"
    DOCUMENT = "document"
    FOLDER = "folder"
    SOURCE = "source"


@dataclass
class KnowledgeMetadata:
    """Metadata for knowledge components"""
    title: str
    type: KnowledgeType
    path: Path
    version: str = "1.0"
    mandatory: bool = False
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class KnowledgeComponent(ABC):
    """
    Component interface for Composite pattern.
    
    Both individual knowledge items (Leaf) and collections (Composite)
    implement this interface.
    """
    
    def __init__(self, metadata: KnowledgeMetadata):
        self.metadata = metadata
        self.loaded = False
    
    @abstractmethod
    def load(self) -> bool:
        """Load the knowledge component"""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Display the component (for debugging/visualization)"""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List['KnowledgeComponent']:
        """Search for components matching query"""
        pass
    
    @abstractmethod
    def get_all_paths(self) -> List[Path]:
        """Get all file paths in this component"""
        pass
    
    def is_loaded(self) -> bool:
        """Check if component is loaded"""
        return self.loaded


class Document(KnowledgeComponent):
    """
    Leaf in Composite pattern - represents a single document.
    """
    
    def __init__(self, metadata: KnowledgeMetadata):
        super().__init__(metadata)
        self.content: Optional[str] = None
    
    def load(self) -> bool:
        """Load document content from file"""
        try:
            if not self.metadata.path.exists():
                logger.warning(f"Document not found: {self.metadata.path}")
                return False
            
            with open(self.metadata.path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            
            self.loaded = True
            logger.debug(f"Loaded document: {self.metadata.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load {self.metadata.path}: {e}")
            return False
    
    def display(self, indent: int = 0) -> str:
        """Display document info"""
        prefix = "  " * indent
        status = "✓" if self.loaded else "✗"
        return f"{prefix}[{status}] 📄 {self.metadata.title}"
    
    def search(self, query: str) -> List[KnowledgeComponent]:
        """Search within document"""
        query_lower = query.lower()
        
        # Search in title
        if query_lower in self.metadata.title.lower():
            return [self]
        
        # Search in content (if loaded)
        if self.loaded and self.content and query_lower in self.content.lower():
            return [self]
        
        # Search in tags
        if any(query_lower in tag.lower() for tag in self.metadata.tags):
            return [self]
        
        return []
    
    def get_all_paths(self) -> List[Path]:
        """Get document path"""
        return [self.metadata.path]


class Folder(KnowledgeComponent):
    """
    Composite in Composite pattern - represents a collection of components.
    
    Can contain both Documents (Leaf) and other Folders (Composite).
    """
    
    def __init__(self, metadata: KnowledgeMetadata):
        super().__init__(metadata)
        self.children: List[KnowledgeComponent] = []
    
    def add(self, component: KnowledgeComponent):
        """Add a child component"""
        self.children.append(component)
        logger.debug(f"Added {component.metadata.title} to {self.metadata.title}")
    
    def remove(self, component: KnowledgeComponent):
        """Remove a child component"""
        self.children.remove(component)
        logger.debug(f"Removed {component.metadata.title} from {self.metadata.title}")
    
    def get_child(self, index: int) -> Optional[KnowledgeComponent]:
        """Get child by index"""
        if 0 <= index < len(self.children):
            return self.children[index]
        return None
    
    def load(self) -> bool:
        """Load all children recursively"""
        success = True
        
        for child in self.children:
            if not child.load():
                success = False
        
        self.loaded = success
        logger.info(f"Loaded folder: {self.metadata.title} ({len(self.children)} items)")
        return success
    
    def display(self, indent: int = 0) -> str:
        """Display folder and all children"""
        prefix = "  " * indent
        status = "✓" if self.loaded else "✗"
        result = f"{prefix}[{status}] 📁 {self.metadata.title}\n"
        
        for child in self.children:
            result += child.display(indent + 1) + "\n"
        
        return result.rstrip()
    
    def search(self, query: str) -> List[KnowledgeComponent]:
        """Search in folder and all children"""
        results = []
        
        # Search in folder name
        if query.lower() in self.metadata.title.lower():
            results.append(self)
        
        # Search in all children
        for child in self.children:
            results.extend(child.search(query))
        
        return results
    
    def get_all_paths(self) -> List[Path]:
        """Get all paths in folder recursively"""
        paths = []
        for child in self.children:
            paths.extend(child.get_all_paths())
        return paths


class KnowledgeLoader:
    """
    Main service for loading and managing knowledge.
    
    Uses Composite pattern to handle hierarchical knowledge structure.
    """
    
    def __init__(self, base_path: Path):
        """
        Args:
            base_path: Root directory for knowledge files
        """
        self.base_path = Path(base_path)
        self.root: Optional[Folder] = None
        self.loaded = False
        logger.info(f"KnowledgeLoader initialized with base: {base_path}")
    
    def build_knowledge_tree(self) -> Folder:
        """
        Build knowledge tree structure.
        
        Returns:
            Root folder containing all knowledge
        """
        root = Folder(KnowledgeMetadata(
            title="MOTHER Knowledge Base",
            type=KnowledgeType.FOLDER,
            path=self.base_path
        ))
        
        # Core Principles (P1-P7)
        principles = self._load_principles()
        if principles:
            root.add(principles)
        
        # Reference Documents
        references = self._load_references()
        if references:
            root.add(references)
        
        # Study Materials
        studies = self._load_studies()
        if studies:
            root.add(studies)
        
        self.root = root
        return root
    
    def _load_principles(self) -> Optional[Folder]:
        """Load P1-P7 principles"""
        principles_path = self.base_path / "core"
        if not principles_path.exists():
            logger.warning(f"Principles directory not found: {principles_path}")
            return None
        
        folder = Folder(KnowledgeMetadata(
            title="Principles (P1-P7)",
            type=KnowledgeType.FOLDER,
            path=principles_path,
            mandatory=True
        ))
        
        # Load P1-P7 files
        for i in range(1, 8):
            principle_files = list(principles_path.glob(f"P{i}_*.md"))
            for file in principle_files:
                doc = Document(KnowledgeMetadata(
                    title=f"P{i}: {file.stem.replace(f'P{i}_', '').replace('_', ' ').title()}",
                    type=KnowledgeType.PRINCIPLE,
                    path=file,
                    mandatory=True,
                    tags=[f"P{i}", "principle", "enforcement"]
                ))
                folder.add(doc)
        
        return folder if folder.children else None
    
    def _load_references(self) -> Optional[Folder]:
        """Load reference documents"""
        ref_path = self.base_path / "docs" / "reference"
        if not ref_path.exists():
            return None
        
        folder = Folder(KnowledgeMetadata(
            title="Reference Documents",
            type=KnowledgeType.FOLDER,
            path=ref_path
        ))
        
        for file in ref_path.glob("*.md"):
            doc = Document(KnowledgeMetadata(
                title=file.stem.replace('_', ' ').title(),
                type=KnowledgeType.DOCUMENT,
                path=file,
                tags=["reference", "documentation"]
            ))
            folder.add(doc)
        
        return folder if folder.children else None
    
    def _load_studies(self) -> Optional[Folder]:
        """Load study materials"""
        study_path = self.base_path / "study_materials"
        if not study_path.exists():
            return None
        
        folder = Folder(KnowledgeMetadata(
            title="Study Materials",
            type=KnowledgeType.FOLDER,
            path=study_path
        ))
        
        for file in study_path.glob("*.md"):
            doc = Document(KnowledgeMetadata(
                title=file.stem.replace('_', ' ').title(),
                type=KnowledgeType.SOURCE,
                path=file,
                tags=["study", "research", "source"]
            ))
            folder.add(doc)
        
        return folder if folder.children else None
    
    def load_all(self) -> bool:
        """
        Load all knowledge.
        
        Returns:
            True if all mandatory knowledge loaded successfully
        """
        if not self.root:
            self.build_knowledge_tree()
        
        success = self.root.load()
        self.loaded = success
        
        if success:
            logger.info("✓ All knowledge loaded successfully")
        else:
            logger.warning("⚠ Some knowledge failed to load")
        
        return success
    
    def search(self, query: str) -> List[KnowledgeComponent]:
        """
        Search knowledge base.
        
        Args:
            query: Search query
        
        Returns:
            List of matching components
        """
        if not self.root:
            logger.warning("Knowledge not loaded, building tree...")
            self.build_knowledge_tree()
        
        return self.root.search(query)
    
    def display_tree(self) -> str:
        """Display knowledge tree"""
        if not self.root:
            return "Knowledge tree not built"
        return self.root.display()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        if not self.root:
            return {"error": "Knowledge not loaded"}
        
        all_paths = self.root.get_all_paths()
        
        return {
            "total_files": len(all_paths),
            "loaded": self.loaded,
            "base_path": str(self.base_path),
            "tree": self.display_tree()
        }


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create loader
    loader = KnowledgeLoader(Path("/home/ubuntu/manus_global_knowledge"))
    
    # Build and load knowledge
    loader.build_knowledge_tree()
    loader.load_all()
    
    # Display tree
    print("\n=== Knowledge Tree ===")
    print(loader.display_tree())
    
    # Search
    print("\n=== Search Results for 'P1' ===")
    results = loader.search("P1")
    for result in results:
        print(f"  - {result.metadata.title}")
    
    # Statistics
    print("\n=== Statistics ===")
    stats = loader.get_statistics()
    print(f"Total files: {stats['total_files']}")
    print(f"Loaded: {stats['loaded']}")
