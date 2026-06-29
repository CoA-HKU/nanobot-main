# knowledge_tool.py - Simple MCI Knowledge Search

import os
from pathlib import Path

def search_mci(query: str) -> str:
    """Search the MCI knowledge base for information."""
    
    home = Path(os.environ.get("USERPROFILE", "."))
    knowledge_dir = home / ".nanobot" / "knowledge"
    
    results = []
    
    # Search all text files in the knowledge folder
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
    
    return "\n\n".join(results[:2]) if results else "小安暫時冇呢個資訊。我嘅知識庫暫時只有腦退化症嘅基本資料。"

TOOLS = [
    {
        "name": "search_mci",
        "description": "Search MCI knowledge base for information",
        "function": search_mci,
    }
]