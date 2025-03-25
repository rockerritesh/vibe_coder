import sys
import os
import re
import requests
import time
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to scrape a website and convert it to markdown
def scrape_website(url, output_dir=None, image_download=False, wait_time=5):
    # Set up headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    
    try:
        with webdriver.Chrome(options=options) as driver:
            print(f"Loading page: {url}")
            driver.get(url)
            
            # Wait for the page to load completely
            try:
                WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                # Extra time for JavaScript to render
                time.sleep(2)
            except TimeoutException:
                print("Page took too long to load, proceeding anyway")
            
            # Create output directory for images if needed
            if image_download and output_dir:
                img_dir = os.path.join(output_dir, "images")
                os.makedirs(img_dir, exist_ok=True)
            
            markdown_content = []
            
            # Get page title
            title = driver.title
            markdown_content.append(f"# {title}\n\n")
            
            # Extract main content
            main_content = driver.find_element(By.TAG_NAME, "body")
            
            # Process all elements in order
            process_element(main_content, markdown_content, driver, url, output_dir, image_download)
            
            return "\n".join(markdown_content)
    
    except WebDriverException as e:
        print(f"Failed to open browser: {e}")
        return None

def process_element(element, markdown_list, driver, base_url, output_dir=None, image_download=False, depth=0):
    """Process an element and its children, adding markdown to the list"""
    # Skip script, style, and hidden elements
    if element.tag_name in ["script", "style", "noscript"]:
        return
    
    # Check if element is hidden
    try:
        if not element.is_displayed():
            return
    except:
        pass  # If we can't determine, continue anyway
    
    # Get text content of this element (excluding children)
    element_text = get_direct_text(element, driver).strip()
    
    # Process by tag name
    tag = element.tag_name
    
    # Headings
    if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        level = int(tag[1])
        if element_text:
            markdown_list.append(f"{'#' * level} {element_text}\n")
    
    # Paragraphs
    elif tag == "p":
        if element_text:
            markdown_list.append(f"{element_text}\n\n")
    
    # Lists
    elif tag == "ul":
        markdown_list.append("\n")
    elif tag == "ol":
        markdown_list.append("\n")
    elif tag == "li":
        bullet = "* " if depth % 2 == 0 else "- "
        if element_text:
            markdown_list.append(f"{bullet}{element_text}\n")
    
    # Links
    elif tag == "a":
        href = element.get_attribute("href")
        if href and element_text:
            # Create proper absolute URL
            abs_url = urljoin(base_url, href)
            markdown_list.append(f"[{element_text}]({abs_url})")
    
    # Images
    elif tag == "img":
        src = element.get_attribute("src")
        alt = element.get_attribute("alt") or "image"
        
        if src:
            # Create proper absolute URL for the image
            img_url = urljoin(base_url, src)
            
            # Download image if requested
            if image_download and output_dir:
                try:
                    img_filename = os.path.basename(urlparse(img_url).path) or f"image_{hash(img_url)}.jpg"
                    img_path = os.path.join(output_dir, "images", img_filename)
                    
                    # Download the image
                    img_data = requests.get(img_url, timeout=5).content
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_data)
                    
                    # Use local reference in markdown
                    markdown_list.append(f"![{alt}](images/{img_filename})\n\n")
                except Exception as e:
                    print(f"Failed to download image {img_url}: {e}")
                    markdown_list.append(f"![{alt}]({img_url})\n\n")
            else:
                # Just link to the image
                markdown_list.append(f"![{alt}]({img_url})\n\n")
    
    # Tables
    elif tag == "table":
        markdown_list.append("\n\n")
        # Will be handled by processing tr and td elements
    
    elif tag == "tr":
        if markdown_list[-1] != "\n" and markdown_list[-1] != "\n\n":
            markdown_list.append("\n")
    
    elif tag == "th":
        if element_text:
            markdown_list.append(f"| **{element_text}** ")
    
    elif tag == "td":
        if element_text:
            markdown_list.append(f"| {element_text} ")
    
    # Code blocks
    elif tag in ["pre", "code"]:
        if element_text:
            markdown_list.append(f"```\n{element_text}\n```\n\n")
    
    # Blockquotes
    elif tag == "blockquote":
        if element_text:
            quoted_text = element_text.replace("\n", "\n> ")
            markdown_list.append(f"> {quoted_text}\n\n")
    
    # Process all children
    try:
        children = element.find_elements(By.XPATH, "./*")
        for child in children:
            process_element(child, markdown_list, driver, base_url, output_dir, image_download, depth + 1)
    except:
        pass

def get_direct_text(element, driver):
    """Get text directly from this element, excluding child elements"""
    try:
        # JavaScript to get direct text content
        script = """
        return Array.from(arguments[0].childNodes)
            .filter(node => node.nodeType === Node.TEXT_NODE)
            .map(node => node.textContent.trim())
            .join(' ')
            .replace(/\\s+/g, ' ')
            .trim();
        """
        return driver.execute_script(script, element)
    except:
        return ""

def main():
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <URL> [output_dir]")
        return
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    print(f"Scraping {url}...")
    markdown_content = scrape_website(url, output_dir, image_download=True)
    
    if markdown_content:
        if output_dir:
            # Create sanitized filename from URL
            domain = urlparse(url).netloc
            filename = f"{domain.replace('.', '_')}_scrape.md"
            output_path = os.path.join(output_dir, filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Content saved to {output_path}")
        else:
            print(markdown_content)

if __name__ == "__main__":
    main()