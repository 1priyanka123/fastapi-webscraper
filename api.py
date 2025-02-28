from fastapi import FastAPI, Query
from typing import Dict, List
from webscrap import scrape_website  # Import the scraper function
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["192.168.31.141"],  # Allows all domains (change this for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# File to store scraped data
SCRAPED_DATA_FILE = "scraped_data.json"

# Function to save scraped data
def save_scraped_data(data):
    try:
        with open(SCRAPED_DATA_FILE, "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)  # Append new data
    with open(SCRAPED_DATA_FILE, "w") as file:
        json.dump(existing_data, file, indent=4)

# Function to load stored data
def load_scraped_data():
    try:
        with open(SCRAPED_DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@app.get("/")
def home():
    return {"message": "Web Scraper API is running!"}

@app.get("/scrape", response_model=Dict)
def get_scraped_data(url: str = Query(..., title="Website URL", description="URL of the website to scrape")):
    """
    Fetch scraped data from the provided URL and store it.
    """
    scraped_data = scrape_website(url)
    save_scraped_data(scraped_data)  # Save to file
    return scraped_data

@app.get("/scraped-data", response_model=List[Dict])
def get_stored_scraped_data():
    """
    Retrieve all previously scraped data.
    """
    return load_scraped_data()