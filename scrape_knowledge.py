import requests
from bs4 import BeautifulSoup
from pathlib import Path

# 1. Define the target URL
url = 'https://www.jccpa.org.hk/about-dementia/'

# 2. Where to save the file (your .nanobot knowledge folder)
knowledge_dir = Path("C:/Users/user/.nanobot/knowledge")
knowledge_dir.mkdir(parents=True, exist_ok=True)
file_path = knowledge_dir / "jccpa_dementia.txt"

print(f"⏳ Fetching content from: {url}")

try:
    # 3. Fetch the webpage
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    
    # 4. Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 5. Extract text
    page_text = soup.get_text(separator='\n', strip=True)
    
    # 6. Save to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# Source: {url}\n\n")
        f.write(page_text)
    
    print(f"✅ Content saved to: {file_path}")

except Exception as e:
    print(f"❌ Error: {e}")