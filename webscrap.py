from flask import Flask, request, jsonify, send_file
import requests
import csv
import json
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re

app = Flask(__name__)


def scrape_website(url):
    """Scrapes all content from the given URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all text content
            text_content = soup.get_text(separator='\n', strip=True)

            # Extract all links
            links = [a['href'] for a in soup.find_all('a', href=True)]

            # Extract all images
            images = [img['src'] for img in soup.find_all('img', src=True)]

            return {
                "url": url,
                "timestamp": datetime.utcnow().isoformat(),
                "text_content": text_content,
                "links": links,
                "images": images
            }
        else:
            return {"error": "Failed to retrieve the webpage"}
    except Exception as e:
        return {"error": str(e)}


@app.route('/scrape', methods=['GET'])
def scrape():
    """API endpoint for scraping any website based on user input."""
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Please provide a URL"}), 400

    data = scrape_website(url)
    return jsonify(data)


if __name__ == '__main__':
    print("Starting the web scraper API...")
    app.run(debug=True)
