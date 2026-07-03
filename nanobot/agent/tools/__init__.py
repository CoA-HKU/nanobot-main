"""Agent tools module."""

from nanobot.agent.tools.base import Schema, Tool, tool_parameters
from nanobot.agent.tools.context import ToolContext
from nanobot.agent.tools.loader import ToolLoader
from nanobot.agent.tools.registry import ToolRegistry
from nanobot.agent.tools.schema import (
    ArraySchema,
    BooleanSchema,
    IntegerSchema,
    NumberSchema,
    ObjectSchema,
    StringSchema,
    tool_parameters_schema,
)

# ============================================================
# CUSTOM MCI TOOLS
# ============================================================
from pathlib import Path
import os

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

# Custom tools list
CUSTOM_TOOLS = [
    {"name": "search_resources", "function": search_resources, "description": "Search for center locations, contact info, transport, and opening hours"},
    {"name": "search_medication", "function": search_medication, "description": "Search for medication information, side effects, dosage, and interactions"},
    {"name": "search_cognitive", "function": search_cognitive, "description": "Search for cognitive training exercises and activity plans"},
    {"name": "search_psychological", "function": search_psychological, "description": "Search for psychological support, coping strategies, and anxiety management"},
]

# Register custom tools
try:
    registry = ToolRegistry()
    for tool in CUSTOM_TOOLS:
        registry.register(
            name=tool["name"],
            func=tool["function"],
            description=tool["description"]
        )
    print(f"✅ Registered {len(CUSTOM_TOOLS)} custom MCI tools")
except Exception as e:
    print(f"❌ Failed to register custom tools: {e}")

__all__ = [
    "Schema",
    "ArraySchema",
    "BooleanSchema",
    "IntegerSchema",
    "NumberSchema",
    "ObjectSchema",
    "StringSchema",
    "Tool",
    "ToolContext",
    "ToolLoader",
    "ToolRegistry",
    "tool_parameters",
    "tool_parameters_schema",
    "CUSTOM_TOOLS",
]