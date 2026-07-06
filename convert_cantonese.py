import os
import re

# Cantonese → Formal Chinese mapping
CANTONESE_TO_FORMAL = {
    # Common particles
    "嘅": "的",
    "冇": "沒有",
    "係": "是",
    "咗": "了",
    "啲": "些",
    "嗰": "那",
    "呢": "這",
    
    # Negative
    "唔": "不",
    "唔好": "不好",
    
    # Verbs
    "畀": "給予",
    "食": "服用",
    "瞓": "睡",
    "睇": "看",
    "講": "說",
    "問": "詢問",
    "幫": "幫助",
    "俾": "給",
    
    # Question patterns
    "點樣": "怎麼樣",
    "有冇": "有沒有",
    "幾多": "多少",
    "邊個": "哪個",
    "邊度": "哪裡",
    "幾時": "何時",
    
    # Others
    "試吓": "試試",
    "話我知": "告訴我",
    "同": "與",
    "仲": "還",
    "好唔好": "好不好",
    "得唔得": "可不可以",
    "乜": "什麼",
    "咩": "什麼",
    "嘢": "東西",
    "人哋": "別人",
    "點解": "為什麼",
}

def convert_text(text):
    """Convert Cantonese text to formal written Chinese."""
    # Sort by length (longest first) to avoid partial matches
    for canto, formal in sorted(CANTONESE_TO_FORMAL.items(), key=lambda x: -len(x[0])):
        text = text.replace(canto, formal)
    return text

def convert_file(input_path, output_path=None):
    """Convert a file from Cantonese to formal written Chinese."""
    if output_path is None:
        output_path = input_path.replace('.txt', '_formal.txt')
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    converted = convert_text(content)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print(f"✅ Converted: {input_path} → {output_path}")
    return output_path

def convert_directory(directory_path):
    """Convert all .txt files in a directory."""
    txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    
    if not txt_files:
        print("❌ No .txt files found in directory.")
        return
    
    for filename in txt_files:
        input_path = os.path.join(directory_path, filename)
        output_path = os.path.join(directory_path, filename.replace('.txt', '_formal.txt'))
        convert_file(input_path, output_path)
    
    print(f"\n✅ Converted {len(txt_files)} files.")

if __name__ == "__main__":
    # Change this path to your knowledge directory
    knowledge_dir = r"C:\Users\user\.nanobot\knowledge"
    
    if os.path.exists(knowledge_dir):
        convert_directory(knowledge_dir)
    else:
        print(f"❌ Directory not found: {knowledge_dir}")
        print("Please update the 'knowledge_dir' path to your actual knowledge folder.")