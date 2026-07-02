# knowledge_tool.py - Multi-RAG Knowledge Search with Embeddings

import os
from pathlib import Path
import numpy as np

# Try to import embedding libraries (fallback to keyword search if not available)
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️ sentence-transformers not installed. Using keyword search only.")
    print("   Install with: py -3.14 -m pip install sentence-transformers scikit-learn")

# --- Embedding Search Class ---
class EmbeddingSearch:
    def __init__(self):
        self.model = None
        self.chunks = []
        self.chunk_embeddings = []
        self.knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"
        self._is_initialized = False
        
        if EMBEDDINGS_AVAILABLE:
            try:
                # Load a lightweight model (works offline, ~80MB)
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self._index_files()
                self._is_initialized = True
                print(f"✅ Embedding search initialized with {len(self.chunks)} chunks")
            except Exception as e:
                print(f"⚠️ Failed to initialize embeddings: {e}")
    
    def _chunk_text(self, text, chunk_size=300, overlap=50):
        """Split text into overlapping chunks."""
        # Split by sentences first
        sentences = text.replace('。', '。\n').replace('！', '！\n').replace('？', '？\n').split('\n')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sent in sentences:
            sent_len = len(sent)
            if current_length + sent_len > chunk_size and current_chunk:
                chunks.append(''.join(current_chunk))
                # Keep overlap
                overlap_text = ''.join(current_chunk[-overlap:]) if overlap > 0 else ''
                current_chunk = [overlap_text] if overlap_text else []
                current_length = len(overlap_text)
            current_chunk.append(sent)
            current_length += sent_len
        
        if current_chunk:
            chunks.append(''.join(current_chunk))
        
        return chunks
    
    def _index_files(self):
        """Index all knowledge files with chunking."""
        all_texts = []
        all_sources = []
        
        for file in self.knowledge_dir.glob("*.txt"):
            try:
                content = file.read_text(encoding='utf-8', errors='ignore')
                # Remove metadata lines
                lines = [l for l in content.split('\n') if not l.startswith('#')]
                clean_text = ' '.join(lines)
                
                # Chunk the text
                chunks = self._chunk_text(clean_text)
                for chunk in chunks:
                    if len(chunk) > 30:  # Ignore very short chunks
                        all_texts.append(chunk)
                        all_sources.append(file.name)
            except:
                continue
        
        if all_texts and self.model:
            self.chunks = [{'text': t, 'source': s} for t, s in zip(all_texts, all_sources)]
            self.chunk_embeddings = self.model.encode(all_texts, show_progress_bar=False)
    
    def search(self, query, top_k=3, min_score=0.3):
        """Search for the most relevant chunks using embeddings."""
        if not self._is_initialized or not self.chunks:
            return None
        
        try:
            query_embedding = self.model.encode([query])[0]
            scores = cosine_similarity([query_embedding], self.chunk_embeddings)[0]
            
            # Get top-k results
            top_indices = np.argsort(scores)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if scores[idx] >= min_score:
                    results.append(f"📄 {self.chunks[idx]['source']}: {self.chunks[idx]['text'][:200]}...")
            
            return results if results else None
        except Exception:
            return None

# --- Initialize embedding search ---
_embedding_search = EmbeddingSearch()

# --- Helper function to search with hybrid approach ---
def _search_with_embeddings(query, top_k=3):
    """Use embeddings to find relevant chunks."""
    if _embedding_search._is_initialized:
        results = _embedding_search.search(query, top_k=top_k)
        if results:
            return "\n\n".join(results)
    return None

def _search_with_keywords(query, file_pattern="*.txt", top_k=2):
    """Fallback keyword search."""
    results = []
    knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"
    
    for file in knowledge_dir.glob(file_pattern):
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            if query.lower() in content.lower():
                lines = content.split('\n')
                for line in lines:
                    if query.lower() in line.lower():
                        results.append(f"📄 {file.name}: {line.strip()}")
        except:
            continue
    
    return "\n\n".join(results[:top_k]) if results else None

# --- 4 RAG Tools (Enhanced with Embeddings) ---

def search_resources(query: str) -> str:
    """Search for center locations, contact info, transport, and opening hours."""
    # Try embeddings first
    result = _search_with_embeddings(query, top_k=2)
    if result:
        return result
    
    # Fallback to keyword search
    result = _search_with_keywords(query, "*.txt", 2)
    if result:
        return result
    
    return "小安暫時冇呢個資源資訊。請聯絡中心查詢。"

def search_medication(query: str) -> str:
    """Search for medication information, side effects, dosage, and interactions."""
    result = _search_with_embeddings(query, top_k=2)
    if result:
        return result
    
    result = _search_with_keywords(query, "*.txt", 2)
    if result:
        return result
    
    return "小安暫時冇呢個藥物資訊。請諮詢醫生或藥劑師。"

def search_cognitive(query: str) -> str:
    """Search for cognitive training exercises and activity plans."""
    result = _search_with_embeddings(query, top_k=2)
    if result:
        return result
    
    result = _search_with_keywords(query, "*.txt", 2)
    if result:
        return result
    
    return "小安暫時冇呢個認知訓練資訊。請諮詢職業治療師。"

def search_psychological(query: str) -> str:
    """Search for psychological support, coping strategies, and anxiety management."""
    result = _search_with_embeddings(query, top_k=2)
    if result:
        return result
    
    result = _search_with_keywords(query, "*.txt", 2)
    if result:
        return result
    
    return "小安暫時冇呢個心理支援資訊。請聯絡專業人士。"

# Register all 4 tools
TOOLS = [
    {
        "name": "search_resources",
        "description": "Search for center locations, contact info, transport, and opening hours",
        "function": search_resources,
    },
    {
        "name": "search_medication",
        "description": "Search for medication information, side effects, dosage, and interactions",
        "function": search_medication,
    },
    {
        "name": "search_cognitive",
        "description": "Search for cognitive training exercises and activity plans",
        "function": search_cognitive,
    },
    {
        "name": "search_psychological",
        "description": "Search for psychological support, coping strategies, and anxiety management",
        "function": search_psychological,
    },
]