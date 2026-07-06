#!/usr/bin/env python3
"""
web_ingest.py - Automated Web Scraper for Dementia Knowledge
Scrapes websites from websites.txt and saves as Markdown
"""

import os
import re
import time
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# ============================================================
# Configuration
# ============================================================

KNOWLEDGE_DIR = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge" / "web"
KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Helper Functions
# ============================================================

def clean_text(text):
    """Clean text by removing extra whitespace"""
    if not text:
        return ""
    # Remove multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Remove extra spaces
    text = re.sub(r' +', ' ', text)
    return text.strip()

def get_clean_filename(url):
    """Generate a clean filename from URL"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    if not path:
        path = 'home'
    # Replace slashes with underscores
    filename = path.replace('/', '_')
    # Remove special characters
    filename = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fff]', '_', filename)
    # Limit length
    if len(filename) > 50:
        filename = filename[:50]
    return filename

def extract_text_with_structure(soup):
    """Extract text while preserving structure (headings, lists, paragraphs)"""
    
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()
    
    # Find main content
    content_selectors = [
        'main', 'article', '.content', '.main-content', 
        '#content', '.post-content', '.entry-content'
    ]
    
    content = None
    for selector in content_selectors:
        element = soup.select_one(selector)
        if element:
            content = element
            break
    
    if not content:
        content = soup.body if soup.body else soup
    
    # Extract text with structure
    return clean_text(content.get_text(separator='\n', strip=True))

def html_to_markdown(html_content):
    """Convert HTML to Markdown"""
    try:
        # Try to convert with markdownify
        markdown = md(html_content, heading_style="ATX")
        return clean_text(markdown)
    except:
        # Fallback: extract text
        soup = BeautifulSoup(html_content, 'html.parser')
        return extract_text_with_structure(soup)

def is_useful_page(soup):
    """Check if page has useful content"""
    text = soup.get_text().strip()
    # Skip pages with very little text
    if len(text) < 100:
        return False
    # Skip admin/login pages
    if any(word in text.lower() for word in ['login', 'sign in', 'register', 'admin']):
        return False
    return True

def should_follow_link(href, base_url, current_path):
    """Check if we should follow this link"""
    if not href:
        return False
    
    # Skip external links
    if href.startswith('http') and not href.startswith(base_url):
        return False
    
    # Skip non-HTML
    if any(href.endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.mp4', '.zip']):
        return False
    
    # Skip common non-content pages
    if any(word in href for word in ['login', 'signin', 'register', 'admin']):
        return False
    
    # Only follow links under the same path (if crawling)
    if current_path and current_path not in href:
        return False
    
    return True

# ============================================================
# Main Scraping Functions
# ============================================================

def scrape_page(url, depth=0, max_depth=3, delay=1, base_url=None):
    """
    Scrape a single page and return content and links
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if page has useful content
        if not is_useful_page(soup):
            return {'content': None, 'links': []}
        
        # Extract content
        content = html_to_markdown(str(soup))
        
        # Get title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else get_clean_filename(url)
        
        # Find links
        links = []
        if depth < max_depth:
            base_url_parsed = urlparse(base_url or url)
            base_domain = f"{base_url_parsed.scheme}://{base_url_parsed.netloc}"
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                
                # Check if we should follow
                parsed = urlparse(full_url)
                if parsed.netloc != base_url_parsed.netloc:
                    continue
                
                # Only follow under the same path
                if base_url and base_url_parsed.path in parsed.path:
                    links.append(full_url)
        
        return {
            'content': content,
            'title': title_text,
            'links': links[:50]  # Limit links
        }
        
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return {'content': None, 'links': []}

def crawl_website(start_url, max_pages=100, max_depth=3, delay=0.5):
    """
    Crawl a website starting from start_url
    """
    print(f"\n🌐 Crawling: {start_url}")
    print(f"   Max pages: {max_pages}, Max depth: {max_depth}")
    
    # Parse base URL for filtering
    parsed = urlparse(start_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    base_path = parsed.path or "/"
    
    visited = set()
    to_visit = [(start_url, 0)]
    scraped = []
    
    while to_visit and len(scraped) < max_pages:
        url, depth = to_visit.pop(0)
        
        if url in visited:
            continue
        visited.add(url)
        
        print(f"   📄 [{depth}] {url[:80]}...")
        
        # Scrape page
        result = scrape_page(url, depth, max_depth, delay, start_url)
        content = result.get('content')
        
        if content and len(content) > 100:
            # Save content
            filename = get_clean_filename(url)
            filepath = KNOWLEDGE_DIR / f"{filename}.md"
            
            # Add source info
            full_content = f"# Source: {url}\n\n{content}"
            filepath.write_text(full_content, encoding='utf-8')
            scraped.append(url)
            print(f"      ✅ Saved: {filepath.name}")
        
        # Add new links
        links = result.get('links', [])
        for link in links:
            if link not in visited and link.startswith(start_url):
                to_visit.append((link, depth + 1))
        
        # Respect delay
        time.sleep(delay)
    
    print(f"   ✅ Crawled {len(scraped)} pages from {start_url}")
    return scraped

def scrape_from_url_file(url_file, max_pages=100, max_depth=3, delay=0.5):
    """
    Read URLs from a file and scrape each
    """
    url_file = Path(url_file)
    if not url_file.exists():
        print(f"❌ URL file not found: {url_file}")
        return []
    
    urls = []
    with open(url_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    
    print(f"📋 Found {len(urls)} URLs to scrape")
    
    all_scraped = []
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processing: {url}")
        scraped = crawl_website(url, max_pages, max_depth, delay)
        all_scraped.extend(scraped)
    
    return all_scraped

# ============================================================
# Command Line Interface
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Automated Web Scraper for Dementia Knowledge")
    parser.add_argument("url", nargs="?", help="Single URL to scrape")
    parser.add_argument("--url-file", default="data/websites.txt", help="File with list of URLs")
    parser.add_argument("--max-pages", type=int, default=100, help="Max pages per website")
    parser.add_argument("--max-depth", type=int, default=3, help="Max crawl depth")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between requests (seconds)")
    parser.add_argument("--no-crawl", action="store_true", help="Don't crawl, only scrape single page")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("🕷️ Automated Web Scraper")
    print("=" * 70)
    print(f"📁 Output directory: {KNOWLEDGE_DIR}")
    print("=" * 70)
    
    if args.url:
        # Single URL
        if args.no_crawl:
            # Just scrape one page
            result = scrape_page(args.url)
            if result.get('content'):
                filename = get_clean_filename(args.url)
                filepath = KNOWLEDGE_DIR / f"{filename}.md"
                content = f"# Source: {args.url}\n\n{result['content']}"
                filepath.write_text(content, encoding='utf-8')
                print(f"✅ Saved: {filepath}")
        else:
            # Crawl website
            crawl_website(args.url, args.max_pages, args.max_depth, args.delay)
    else:
        # Read from URL file
        print(f"\n📋 Reading URLs from: {args.url_file}")
        scrape_from_url_file(args.url_file, args.max_pages, args.max_depth, args.delay)
    
    print("\n" + "=" * 70)
    print("✅ All done!")
    print(f"📁 Files saved to: {KNOWLEDGE_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()