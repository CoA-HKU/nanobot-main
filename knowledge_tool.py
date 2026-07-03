# knowledge_tool.py - Multi-RAG Knowledge Search (Keyword Only - Dashboard Safe)

import os
from pathlib import Path

# --- Embedding Search DISABLED for dashboard compatibility ---
EMBEDDINGS_AVAILABLE = True

# --- Helper function for keyword search ---
def _search_with_keywords(query, file_pattern="*.txt", top_k=2):
    """Keyword search across all knowledge files."""
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

# --- 4 RAG Tools (Keyword Search Only) ---

def search_resources(query: str) -> str:
    """Search for center locations, contact info, transport, and opening hours."""
    result = _search_with_keywords(query, "*.txt", 2)
    if result:
        return result
    return "小安暫時冇呢個資源資訊。請聯絡中心查詢。"

def search_medication(query: str) -> str:
    """Search for medication information, side effects, dosage, and interactions."""
    result = _search_with_keywords(query, "*.txt", 2)
    if result:
        return result
    return "小安暫時冇呢個藥物資訊。請諮詢醫生或藥劑師。"

def search_cognitive(query: str) -> str:
    """Search for cognitive training exercises and activity plans."""
    result = _search_with_keywords(query, "*.txt", 2)
    if result:
        return result
    return "小安暫時冇呢個認知訓練資訊。請諮詢職業治療師。"

def search_psychological(query: str) -> str:
    """Search for psychological support, coping strategies, and anxiety management."""
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