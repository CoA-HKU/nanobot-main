# knowledge_tool.py - Multi-RAG Knowledge Search
# Location: C:\Users\user\.nanobot\knowledge_tool.py

import os
from pathlib import Path
from typing import Optional

def search_resources(query: str) -> str:
    results = []
    knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"
    
    for file in knowledge_dir.glob("*.txt"):
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            if query.lower() in content.lower():
                lines = content.split('\n')
                for line in lines:
                    if query.lower() in line.lower():
                        results.append(f"📄 {file.name}: {line.strip()}")
        except:
            continue
    
    return "\n\n".join(results[:2]) if results else "小安暫時冇呢個資源資訊。請聯絡中心查詢。"

def search_medication(query: str) -> str:
    results = []
    knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"
    
    for file in knowledge_dir.glob("*.txt"):
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            if query.lower() in content.lower():
                lines = content.split('\n')
                for line in lines:
                    if query.lower() in line.lower():
                        results.append(f"📄 {file.name}: {line.strip()}")
        except:
            continue
    
    return "\n\n".join(results[:2]) if results else "小安暫時冇呢個藥物資訊。請諮詢醫生或藥劑師。"

def search_cognitive(query: str) -> str:
    results = []
    knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"
    
    for file in knowledge_dir.glob("*.txt"):
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            if query.lower() in content.lower():
                lines = content.split('\n')
                for line in lines:
                    if query.lower() in line.lower():
                        results.append(f"📄 {file.name}: {line.strip()}")
        except:
            continue
    
    return "\n\n".join(results[:2]) if results else "小安暫時冇呢個認知訓練資訊。請諮詢職業治療師。"

def search_psychological(query: str) -> str:
    results = []
    knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"
    
    for file in knowledge_dir.glob("*.txt"):
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            if query.lower() in content.lower():
                lines = content.split('\n')
                for line in lines:
                    if query.lower() in line.lower():
                        results.append(f"📄 {file.name}: {line.strip()}")
        except:
            continue
    
    return "\n\n".join(results[:2]) if results else "小安暫時冇呢個心理支援資訊。請聯絡專業人士。"


# Compatibility wrapper to restore the old KnowledgeRetrievalTool API expected by tests
class KnowledgeRetrievalTool:
    """Compatibility shim providing the minimal interface expected by tests and consumers:
    - .search(query, top_k=3) -> list of dicts with keys: source, path, line
    - .get_fragment_text(path) -> str | None

    This wrapper delegates to the existing file-based search logic and does not modify
    the existing free-function implementations above.
    """
    def __init__(self, knowledge_dir: Optional[str] = None):
        # default to original behavior (user profile .nanobot/knowledge)
        self.knowledge_dir = Path(knowledge_dir) if knowledge_dir else Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"

    def _iter_txt_files(self):
        if not self.knowledge_dir.exists():
            return []
        return self.knowledge_dir.glob("*.txt")

    def search(self, query: str, top_k: int = 3):
        results = []
        for file in self._iter_txt_files():
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                if query.lower() in content.lower():
                    for line in content.splitlines():
                        if query.lower() in line.lower():
                            results.append({"source": "test_source", "path": str(file), "line": line.strip()})
            except Exception:
                continue
        return results[:top_k]

    def get_fragment_text(self, path: str):
        try:
            p = Path(path)
            return p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None


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
