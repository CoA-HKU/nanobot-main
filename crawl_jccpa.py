import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse
import time

# 1. Where to save the files
knowledge_dir = Path("C:/Users/user/.nanobot/knowledge")
knowledge_dir.mkdir(parents=True, exist_ok=True)

# 2. Define the starting URL
start_url = 'https://www.jccpa.org.hk/about-dementia/'
base_domain = 'https://www.jccpa.org.hk'

print(f"⏳ Starting to crawl: {start_url}")

try:
    # 3. Get the main page
    response = requests.get(start_url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 4. Find all links on the main page
    all_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Convert relative URLs to absolute URLs
        full_url = urljoin(base_domain, href)
        
        # Only keep links that are sub-pages of /about-dementia/
        if '/about-dementia/' in full_url and full_url != start_url:
            # Avoid duplicates and special links
            if full_url not in all_links and not full_url.endswith('.pdf'):
                all_links.append(full_url)

    print(f"✅ Found {len(all_links)} sub-pages to scrape.")

    # 5. Save the main page
    main_text = soup.get_text(separator='\n', strip=True)
    main_file = knowledge_dir / "jccpa_main.txt"
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(f"# Source: {start_url}\n\n")
        f.write(main_text)
    print(f"✅ Saved main page to: {main_file}")

    # 6. Scrape each sub-page
    for i, sub_url in enumerate(all_links, 1):
        try:
            print(f"⏳ Scraping {i}/{len(all_links)}: {sub_url}")
            
            sub_response = requests.get(sub_url, timeout=15)
            sub_response.raise_for_status()
            sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
            
            # Extract text
            sub_text = sub_soup.get_text(separator='\n', strip=True)
            
            # Create a safe filename from the URL
            # e.g., "https://www.jccpa.org.hk/about-dementia/caring-tips/" -> "caring-tips"
            url_path = urlparse(sub_url).path
            filename = url_path.strip('/').replace('/', '_')
            if not filename:
                filename = f"page_{i}"
            
            file_path = knowledge_dir / f"jccpa_{filename}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Source: {sub_url}\n\n")
                f.write(sub_text)
            
            print(f"   ✅ Saved to: {file_path}")
            
            # Be nice to the server — wait a moment between requests
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ❌ Error scraping {sub_url}: {e}")

    print("🎉 All done! Your knowledge base is ready.")

except Exception as e:
    print(f"❌ Error: {e}")