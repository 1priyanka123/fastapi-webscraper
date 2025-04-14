# FastAPI Web Scraper

A simple web scraping API built with FastAPI and BeautifulSoup that allows users to extract data from websites.

## Overview

This project provides a REST API for web scraping using FastAPI. It offers endpoints to scrape data from specified URLs and supports static HTML extraction using CSS selectors. The application returns the scraped data directly in the API response.

## Features

- Fast API endpoints built with FastAPI
- HTML scraping using BeautifulSoup
- Support for basic CSS selector-based extraction
- Simple, lightweight implementation
- Asynchronous request handling

## Requirements

- Python 3.8+
- FastAPI
- BeautifulSoup4
- Uvicorn
- Requests

## Project Structure

```
fastapi-webscraper/
├── app/
│   ├── main.py
│   ├── models.py
│   └── scraper.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/1priyanka123/fastapi-webscraper.git
cd fastapi-webscraper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` and the API documentation at `http://localhost:8000/docs`.

### API Endpoints

- **POST /scrape**: Scrape a website and return the extracted data

### Example: Scraping a website

Using curl:
```bash
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "selectors": {
      "title": "h1",
      "paragraphs": "p"
    }
  }'
```

Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/scrape",
    json={
        "url": "https://example.com",
        "selectors": {
            "title": "h1",
            "paragraphs": "p"
        }
    }
)

print(response.json())
```

## How it Works

1. The client sends a POST request to the `/scrape` endpoint with a URL and CSS selectors
2. The application fetches the HTML content from the specified URL
3. BeautifulSoup parses the HTML and extracts the requested elements
4. The scraped data is returned in JSON format

## Development

### Adding New Features

To extend the scraper functionality:

1. Modify `app/scraper.py` to add new extraction methods
2. Update the API models in `app/models.py` if needed
3. Add new endpoints in `app/main.py`

## Future Enhancements

Potential future improvements:
- Adding data persistence (database storage)
- Implementing user authentication
- Adding scheduled scraping jobs
- Creating a web interface for managing scraping tasks
- Supporting more complex selectors and extraction patterns
- Adding dynamic content extraction for JavaScript-rendered pages (using Playwright or Selenium)

## API Documentation

The FastAPI application comes with automatic interactive API documentation.

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

Access the interactive API documentation at `http://localhost:8000/docs` after starting the application.

## Disclaimer

This tool is intended for educational purposes and legitimate data extraction. Be sure to respect website terms of service and robots.txt rules when scraping websites.

