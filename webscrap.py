from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

app = Flask(__name__)

def clean_text(text):
    """Clean and format the extracted text"""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace and newlines
    text = re.sub(r'[^\w\s.,!?-]', '', text)  # Remove special characters but keep basic punctuation
    return text.strip()

def extract_structured_text(soup):
    """Extract text content in a structured way"""
    structured_content = {
        "title": "",
        "headings": [],
        "paragraphs": [],
        "links": []
    }

    # Extract title
    title_tag = soup.find('title')
    if title_tag:
        structured_content["title"] = clean_text(title_tag.get_text())

    # Extract headings
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        cleaned_heading = clean_text(heading.get_text())
        if cleaned_heading:
            structured_content["headings"].append(cleaned_heading)

    # Extract paragraphs
    for p in soup.find_all('p'):
        cleaned_paragraph = clean_text(p.get_text())
        if cleaned_paragraph:
            structured_content["paragraphs"].append(cleaned_paragraph)

    # Extract links
    for link in soup.find_all('a'):
        link_text = clean_text(link.get_text())
        if link_text:
            structured_content["links"].append(link_text)

    return structured_content  # Move return statement outside of the loop

def scrape_website(url):
    """Scrapes text content from the given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'noscript', 'iframe', 'footer']):
            element.decompose()

        # Extract text in a structured way
        structured_content = extract_structured_text(soup)

        # Get all text content
        all_text = clean_text(soup.get_text(separator=' ', strip=True))

        return {
            "url": url,
            "timestamp": datetime.utcnow().isoformat(),
            "structured_content": structured_content,
            "full_text": all_text,
            "text_length": len(all_text),
            "word_count": len(all_text.split())
        }

    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Scraping failed: {str(e)}"}

@app.route('/scrape', methods=['GET'])
def scrape():
    """API endpoint for scraping text content."""
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    if not url.startswith(('http://', 'https://')):
        return jsonify({"error": "Invalid URL format"}), 400

    data = scrape_website(url)

    if "error" in data:
        return jsonify(data), 500

    return jsonify(data)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    print("Starting the text scraper API...")
    app.run(debug=True)
