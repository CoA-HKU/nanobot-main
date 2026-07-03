import sys
sys.path.insert(0, r'C:\Users\user\.nanobot')

try:
    import knowledge_tool
    print('✅ File loaded successfully!')
    print(f'Tools found: {len(knowledge_tool.TOOLS)}')
    for tool in knowledge_tool.TOOLS:
        print(f'  - {tool["name"]}')
except Exception as e:
    print(f'❌ Error: {e}')