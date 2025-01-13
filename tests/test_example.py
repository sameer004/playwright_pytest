import pytest
import time
from playwright.sync_api import sync_playwright
import logging




def test_example(page_setup):
    page = page_setup
    # Navigate to a reliable website
    page.goto("https://www.google.com")
    
    # Assert the page contains the title "Google"
    assert "Google" in page.title()
    # Take a screenshot
    page.screenshot(path="screenshot.png")
    logging.info("Testing screenshot")
    print("Testing screenshot")
    time.sleep(1)  # Wait for 5 seconds for the screenshot to be saved

