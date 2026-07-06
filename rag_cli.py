#!/usr/bin/env python3
"""
rag_cli.py - CLI tool to test your RAG server
Usage: python rag_cli.py "你的問題"
"""

import sys
import json
import requests

SERVER_URL = "http://localhost:5001"

def chat(message):
    """Send a message to the RAG server"""
    try:
        response = requests.post(
            f"{SERVER_URL}/chat",
            json={"message": message},
            timeout=30
        )
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "❌ Cannot connect to RAG server. Is it running?"}
    except Exception as e:
        return {"error": f"❌ Error: {e}"}

def main():
    if len(sys.argv) < 2:
        print("Usage: python rag_cli.py '你的問題'")
        print("Example: python rag_cli.py '什麼是腦退化症？'")
        print("\nOr try caregiver commands:")
        print("  python rag_cli.py '/setname 陳婆婆'")
        print("  python rag_cli.py '/addpref 喜歡聽粵曲'")
        print("  python rag_cli.py '/calm 一切安好'")
        print("  python rag_cli.py '/profile'")
        sys.exit(1)
    
    message = " ".join(sys.argv[1:])
    print(f"\n👤 用戶: {message}")
    print("=" * 60)
    
    result = chat(message)
    
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        response = result.get('response', 'No response')
        print(f"🤖 小安: {response}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()