"""
IDEN Challenge Product Scraper

This script extracts product data from the IDEN challenge dashboard using Playwright.
It implements session persistence, infinite scrolling, and robust product extraction.

Author: Anant Sharma
Date: August 2025
"""

import json
import time
import sys
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Configuration constants
load_dotenv()  # Load environment variables from .env file

# File and scraping settings
SESSION_FILE = "session.json"
PRODUCTS_FILE = "products.json"
MAX_PRODUCTS = 3751  # Maximum number of products to extract (as shown in the dashboard)

# Authentication credentials
EMAIL = os.getenv("EMAIL", "anant.sharma.career@gmail.com")
PASSWORD = os.getenv("PASSWORD", "dmteYchp")

def log(msg):
    """Print a timestamped log message."""
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")
    sys.stdout.flush()

def click_step(page, label, timeout=8000):
    """
    Try multiple methods to click an element with the given label.
    Returns True if successful, False otherwise.
    """
    log(f"Looking for '{label}'...")
    candidates = [
        lambda: page.get_by_role("button", name=label),
        lambda: page.get_by_text(label),
        lambda: page.locator("button", has_text=label),
    ]
    for finder in candidates:
        try:
            locator = finder()
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            log(f"✓ Clicked '{label}'")
            return True
        except Exception:
            continue
    log(f"⚠ Step '{label}' not found, skipping.")
    return False

def save_session(context):
    """Save the browser context session to a file."""
    log("Saving session...")
    storage = context.storage_state()
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(storage, f)

def load_session():
    """Load a saved browser session if available."""
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def authenticate(context):
    """
    Perform the authentication flow.
    Returns the authenticated page.
    """
    page = context.new_page()
    log("Opening login page...")
    page.goto("https://hiring.idenhq.com/", wait_until="networkidle")

    log("Filling in credentials...")
    page.fill('input[type="email"]', EMAIL)
    page.fill('input[type="password"]', PASSWORD)

    log("Clicking 'Sign in' button...")
    click_step(page, "Sign in")

    # Wait for navigation - handle both possible paths
    try:
        log("Waiting for navigation...")
        page.wait_for_url("**/challenge", timeout=10000)
    except Exception:
        try:
            log("Checking for instructions page...")
            if page.url.find("instructions") > -1 or page.get_by_text("Launch Challenge").count() > 0:
                log("On instructions page, clicking 'Launch Challenge'...")
                click_step(page, "Launch Challenge")
                page.wait_for_url("**/challenge", timeout=10000)
        except Exception as e:
            log(f"Navigation issue: {e}")
            # Take screenshot for debugging
            page.screenshot(path="login_error.png")

    save_session(context)
    return page

def extract_products(page):
    """
    Extract all product cards by scrolling through the lazy-loaded grid.
    Implements robust selector fallbacks to handle varying page structures.
    Returns a list of product dictionaries with structured data.
    """
    # Product grid selector options in order of preference
    container_selectors = [
        ".grid.grid-cols-2.md\\:grid-cols-3.lg\\:grid-cols-4.gap-4",  # Primary selector
        "[class*='grid'][class*='gap']",                              # Generic grid with gap
        "div:has(> div:has(h3))"                                      # Structural selector
    ]
    
    log("Locating product grid...")
    container = None
    
    # Find the product grid using multiple selector strategies
    for selector in container_selectors:
        try:
            potential_container = page.locator(selector).first
            if potential_container and potential_container.count() > 0:
                container = potential_container
                log(f"✓ Found product grid with selector: {selector}")
                break
        except Exception:
            continue
    
    # Fallback to body if no container found
    if not container:
        log("⚠ Could not locate product grid. Using page body as fallback.")
        container = page.locator("body").first
    
    container.wait_for(state="visible", timeout=15000)

    # Data collection variables
    products = []
    seen_ids = set()
    last_height = 0
    scroll_attempts = 0
    max_scroll_attempts = 5  # Stop scrolling if no new products after 5 attempts

    log("Beginning product extraction...")
    page.wait_for_load_state("networkidle")

    # Continue scrolling until we reach MAX_PRODUCTS or no more products load
    while len(products) < MAX_PRODUCTS:
        # Get all product cards in the container
        items = container.locator("> div")
        count = items.count()
        
        log(f"Processing batch of {count} visible products...")
        
        for i in range(count):
            if len(products) >= MAX_PRODUCTS:
                break
                
            try:
                item = items.nth(i)
                
                # Extract product name using multiple selector strategies
                name_selectors = ["h3", "[class*='product-name']", ".h-12", "div.font-bold"]
                name = ""
                for selector in name_selectors:
                    try:
                        name_elem = item.locator(selector).first
                        if name_elem:
                            name = name_elem.inner_text().strip()
                            if name:
                                break
                    except Exception:
                        continue
                
                # Extract ID with multiple strategies
                id_selectors = ["text=/ID:/, [class*='product-id']", "div.font-mono span.font-medium"]
                id_val = ""
                for selector in id_selectors:
                    try:
                        id_elem = item.locator(selector).first
                        if id_elem:
                            id_text = id_elem.inner_text().strip()
                            id_val = id_text.split(":")[-1].strip() if ":" in id_text else id_text
                            if id_val:
                                break
                    except Exception:
                        continue
                
                # Initialize other fields
                description = ""
                weight = ""
                category = ""

                # Extract structured data from the card
                field_selectors = [
                    "div:has-text('Description')", 
                    "div:has-text('Weight')", 
                    "div:has-text('Category')",
                    "div.flex.items-center.justify-between"
                ]
                
                # Try each selector for fields
                for selector in field_selectors:
                    fields = item.locator(selector)
                    field_count = fields.count()
                    
                    for j in range(field_count):
                        try:
                            field_text = fields.nth(j).inner_text().strip()
                            
                            # Extract field values based on key text
                            if "Description:" in field_text:
                                description = field_text.split("Description:")[-1].strip()
                            elif "Weight" in field_text and "kg" in field_text.lower():
                                weight_text = field_text.split("Weight")[1] if "Weight" in field_text else field_text
                                weight = weight_text.split(":")[-1].replace("(kg)", "").replace("kg", "").strip()
                            elif "Category:" in field_text:
                                category = field_text.split("Category:")[-1].strip()
                        except Exception:
                            continue

                # Add product if we have an ID and haven't seen it before
                if id_val and id_val not in seen_ids:
                    products.append({
                        "name": name,
                        "id": id_val,
                        "description": description,
                        "weight": weight,
                        "category": category
                    })
                    seen_ids.add(id_val)
                    log(f"Collected {len(products)} / {MAX_PRODUCTS}: {id_val} | {name}")
            except Exception as e:
                # Just skip this item on error
                continue

        # If we've collected enough products, we're done
        if len(products) >= MAX_PRODUCTS:
            break

        # Scroll faster using JavaScript
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(0.3)
        new_height = page.evaluate("document.body.scrollHeight")
        
        # If page height hasn't changed, we've probably reached the end
        if new_height == last_height:
            scroll_attempts += 1
            if scroll_attempts >= max_scroll_attempts:
                log("End of content detected - no new products after multiple scrolls.")
                break
        else:
            scroll_attempts = 0
            
        last_height = new_height

    return products

def main():
    """Main execution function."""
    try:
        with sync_playwright() as p:
            session_data = load_session()

            # Set the user data directory for persistent context
            user_data_dir = "userdata"

            # Handle existing or new session
            if session_data:
                log("Using existing session...")
                context = p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=False
                )
                # Load session cookies
                context.add_cookies(session_data["cookies"])
                page = context.new_page()
                page.goto("https://hiring.idenhq.com/challenge", wait_until="domcontentloaded")
            else:
                log("No existing session found.")
                context = p.chromium.launch_persistent_context(user_data_dir, headless=False)
                page = authenticate(context)

            # Navigation steps
            for step in ["Start Journey", "Continue Search", "Inventory Section"]:
                if click_step(page, step):
                    page.wait_for_timeout(1000)  # Allow time for any animations
            
            # Wait for the page to stabilize
            page.wait_for_load_state("networkidle")
            
            # Extract all products
            products = extract_products(page)
            log(f"✓ Extraction complete: {len(products)} products collected (limit {MAX_PRODUCTS}).")

            # Save to JSON file
            with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            log(f"✓ Data exported to {PRODUCTS_FILE}")

            context.close()
            
    except Exception as e:
        log(f"⚠ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
