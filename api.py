from fastapi import FastAPI, Query
from typing import Dict
from webscrap import scrape_website  # Import the scraper function

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Web Scraper API is running!"}

@app.get("/scrape", response_model=Dict)
def get_scraped_data(url: str = Query(..., title="Website URL", description="URL of the website to scrape")):
    """
    Fetch scraped data from the provided URL.
    """
    scraped_data = scrape_website(url)
    return scraped_data
