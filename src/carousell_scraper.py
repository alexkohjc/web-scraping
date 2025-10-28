"""
Carousell.sg Web Scraper
Scrapes product listings from Carousell.sg search results
"""

import time
import random
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class CarousellScraper:
    """Scraper for Carousell.sg marketplace"""

    def __init__(self, headless: bool = True, delay_range: tuple = (2, 5), browser: Optional[str] = None):
        """
        Initialize the scraper

        Args:
            headless: Run browser in headless mode
            delay_range: Tuple of (min, max) seconds for random delays
            browser: Browser to use ('chrome', 'firefox', or None for auto-detect)
        """
        self.headless = headless
        self.delay_range = delay_range
        self.base_url = "https://www.carousell.sg"
        self.driver = None
        self.browser = browser
        self.debug_screenshot = None  # Store screenshot bytes for debugging

    def _detect_browser(self) -> Optional[str]:
        """Detect which browser is available on the system"""
        browsers = {
            'chrome': ['google-chrome', 'chrome', 'chromium', 'chromium-browser'],
            'firefox': ['firefox'],
        }

        for browser_name, commands in browsers.items():
            for cmd in commands:
                if shutil.which(cmd):
                    print(f"Detected {browser_name} browser: {cmd}")
                    return browser_name

        return None

    def _setup_driver(self):
        """Setup browser driver with appropriate options"""
        # Determine which browser to use
        browser = self.browser or self._detect_browser()

        if not browser:
            raise RuntimeError(
                "No supported browser found. Please install Chrome/Chromium or Firefox.\n"
                "For WSL2/Ubuntu:\n"
                "  Chrome: sudo apt update && sudo apt install -y chromium-browser\n"
                "  Firefox: sudo apt update && sudo apt install -y firefox\n"
            )

        if browser == 'chrome':
            self._setup_chrome()
        elif browser == 'firefox':
            self._setup_firefox()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    def _setup_chrome(self):
        """Setup Chrome/Chromium driver"""
        from selenium.webdriver.chrome.options import Options
        import tempfile

        print("Setting up Chrome driver...")
        chrome_options = Options()

        if self.headless:
            print("⚠️  Warning: Headless mode may trigger CAPTCHA. Consider disabling it for better results.")
            chrome_options.add_argument("--headless=new")

        # Essential options for WSL2 compatibility
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # Fix for DevToolsActivePort error - use unique port
        debug_port = random.randint(9000, 9999)
        chrome_options.add_argument(f"--remote-debugging-port={debug_port}")

        # Create temporary user data directory to avoid conflicts
        user_data_dir = tempfile.mkdtemp(prefix="chrome_profile_")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        # Minimal additional flags for stability
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--no-first-run")

        # Suppress unnecessary logging
        chrome_options.add_argument("--log-level=3")

        # Set page load strategy to 'eager' for faster loading
        chrome_options.page_load_strategy = 'eager'

        # Try to find chromium binary
        chromium_paths = [
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
            '/snap/bin/chromium',
            '/usr/bin/google-chrome',
            '/usr/bin/chrome',
        ]

        for path in chromium_paths:
            if shutil.which(path) or Path(path).exists():
                print(f"Found browser at: {path}")
                chrome_options.binary_location = path
                break

        print(f"Initializing ChromeDriver (debug port {debug_port})...")
        if not self.headless:
            print("Running in visible mode - browser window will open")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Error initializing ChromeDriver: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure Chromium is installed: sudo apt install chromium-browser")
            print("2. Or try Firefox: sudo apt install firefox")
            raise

        # Set timeouts to prevent hanging
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(3)

        print("✓ Chrome driver setup complete!")

    def _setup_firefox(self):
        """Setup Firefox driver"""
        try:
            from selenium.webdriver.firefox.options import Options

            print("Setting up Firefox driver...")
            firefox_options = Options()

            if self.headless:
                firefox_options.add_argument("--headless")

            # Use Selenium Manager to auto-download GeckoDriver
            self.driver = webdriver.Firefox(options=firefox_options)

            # Set timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(3)

            print("Firefox driver setup complete!")

        except Exception as e:
            raise RuntimeError(f"Failed to setup Firefox driver: {e}")

    def _random_delay(self):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        print(f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)

    def _scroll_page(self, scrolls: int = 3, delay: tuple = (0.5, 1.0)):
        """
        Scroll the page to load more content

        Args:
            scrolls: Number of times to scroll
            delay: Tuple of (min, max) seconds to wait between scrolls
        """
        for i in range(scrolls):
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(delay[0], delay[1]))
            print(f"Scrolled {i+1}/{scrolls} times")

    def search(self, query: str, max_results: int = 20) -> List[Dict[str, str]]:
        """
        Search for items on Carousell

        Args:
            query: Search term
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing item information
        """
        results = []

        try:
            # Setup driver if not already done
            if self.driver is None:
                print("Setting up Chrome driver...")
                self._setup_driver()

            # Build search URL
            search_url = f"{self.base_url}/search/{query.replace(' ', '%20')}"
            print(f"Navigating to: {search_url}")

            try:
                self.driver.get(search_url)
                print("Page loaded successfully")
            except TimeoutException:
                print("Page load timeout - continuing anyway...")
            except Exception as e:
                print(f"Error loading page: {e}")
                raise

            print("Waiting for page to settle...")
            time.sleep(0.5)  # Reduced wait time for faster scraping

            # Check if page actually loaded
            try:
                page_title = self.driver.title
                print(f"Page title: {page_title}")
            except:
                print("Could not get page title")

            # Scroll to load more items (skip if max_results is small)
            if max_results > 10:
                print("Scrolling to load more items...")
                self._scroll_page(scrolls=2)
            else:
                print("Skipping scroll for small result set")

            # Wait for listings to load
            print("Waiting for page content to load...")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                print("Body element found")
            except TimeoutException:
                print("Timeout waiting for page body to load")
                return results

            # Try different selectors to find product listings
            # Carousell's structure may vary, so we'll try multiple approaches
            print("Searching for product listings on page...")

            # Approach 1: Look for article tags or product cards
            listing_selectors = [
                'article',
                '[data-testid*="listing"]',
                '[class*="ProductCard"]',
                '[class*="ListingCard"]',
                'a[href*="/p/"]',  # Links to product pages
            ]

            all_listings = []
            for selector in listing_selectors:
                try:
                    print(f"Trying selector: {selector}")
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"✓ Found {len(elements)} elements with selector: {selector}")
                        all_listings = elements
                        break
                    else:
                        print(f"  No elements found with: {selector}")
                except Exception as e:
                    print(f"  Error with selector {selector}: {e}")
                    continue

            if not all_listings:
                print("Could not find any product listings. The page structure may have changed.")
                # Save screenshot for debugging
                try:
                    self.debug_screenshot = self.driver.get_screenshot_as_png()
                    print(f"Saved debug screenshot in memory")
                    print(f"Current URL: {self.driver.current_url}")
                    print(f"Page title: {self.driver.title}")
                except Exception as e:
                    print(f"Could not capture screenshot: {e}")
                return results

            print(f"Processing {min(len(all_listings), max_results)} listings...")

            # Temporarily disable implicit wait for faster extraction
            self.driver.implicitly_wait(0)


            # Extract information from each listing
            for idx, listing in enumerate(all_listings[:max_results]):
                try:
                    item_data = {}

                    # Get all text content for debugging
                    listing_text = listing.text

                    # Try to extract the link (URL)
                    try:
                        # Look for link element
                        if listing.tag_name == 'a':
                            link_elem = listing
                        else:
                            links = listing.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')
                            link_elem = links[0] if links else None

                        if link_elem:
                            item_url = link_elem.get_attribute('href')
                            if item_url and not item_url.startswith('http'):
                                item_url = self.base_url + item_url
                            item_data['url'] = item_url
                        else:
                            item_data['url'] = 'N/A'
                    except:
                        item_data['url'] = 'N/A'

                    # Try to extract the title/name with more comprehensive selectors
                    try:
                        # Try multiple selectors for title
                        title_selectors = [
                            'h3', 'h4', 'h2',
                            'p[class*="title"]',
                            '[class*="Title"]',
                            '[class*="ProductCard"]',
                            '[data-testid*="title"]',
                            '[class*="name"]',
                            'div[class*="D_zW"]',  # Common Carousell pattern
                            'p[class*="D_"]',
                        ]
                        title_text = None
                        for sel in title_selectors:
                            elems = listing.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                for elem in elems:
                                    text = elem.text.strip()
                                    # Skip if it looks like a price
                                    if text and '$' not in text and len(text) > 3:
                                        title_text = text
                                        break
                                if title_text:
                                    break

                        # Fallback: parse from all text
                        if not title_text and listing_text:
                            lines = [line.strip() for line in listing_text.split('\n') if line.strip()]
                            # Look for the first line that's not a price, seller, or time
                            for line in lines:
                                if line and '$' not in line and not any(x in line.lower() for x in ['ago', 'hour', 'minute', 'day', 'week', 'month']):
                                    if len(line) > 3:  # Reasonable title length
                                        title_text = line
                                        break

                        item_data['name'] = title_text if title_text else 'N/A'
                    except Exception as e:
                        print(f"Error extracting name: {e}")
                        item_data['name'] = 'N/A'

                    # Try to extract the price with regex
                    try:
                        import re
                        price_text = None

                        # Try CSS selectors first
                        price_selectors = [
                            '[class*="price"]',
                            '[class*="Price"]',
                            '[data-testid*="price"]',
                            'p[class*="D_"]',
                            'span[class*="D_"]',
                        ]

                        for sel in price_selectors:
                            elems = listing.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                for elem in elems:
                                    text = elem.text.strip()
                                    if '$' in text:
                                        price_text = text
                                        break
                                if price_text:
                                    break

                        # Fallback: search in all text for price pattern
                        if not price_text and listing_text:
                            # Match patterns like: $100, S$100, $1,000, $10.50, etc.
                            price_match = re.search(r'S?\$\s*[\d,]+(?:\.\d{2})?', listing_text)
                            if price_match:
                                price_text = price_match.group()

                        item_data['price'] = price_text if price_text else 'N/A'
                    except Exception as e:
                        print(f"Error extracting price: {e}")
                        item_data['price'] = 'N/A'

                    # Try to extract seller name
                    try:
                        import re
                        seller_name = None

                        # Try CSS selectors
                        seller_selectors = [
                            '[class*="seller"]',
                            '[class*="Seller"]',
                            '[class*="username"]',
                            '[class*="Username"]',
                            '[data-testid*="seller"]',
                            'a[href*="/u/"]',  # User profile links
                        ]

                        for sel in seller_selectors:
                            elems = listing.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                text = elems[0].text.strip()
                                if text and len(text) > 0:
                                    seller_name = text
                                    break

                        # Fallback: look for @username pattern or text near time
                        if not seller_name and listing_text:
                            lines = [line.strip() for line in listing_text.split('\n') if line.strip()]
                            for line in lines:
                                # Look for @username
                                if line.startswith('@'):
                                    seller_name = line
                                    break
                                # Look for username near time indicators
                                if any(x in line.lower() for x in ['ago', 'hour', 'minute', 'day']):
                                    # Previous line might be seller
                                    idx_line = lines.index(line)
                                    if idx_line > 0:
                                        potential_seller = lines[idx_line - 1]
                                        if '$' not in potential_seller and len(potential_seller) < 50:
                                            seller_name = potential_seller
                                            break

                        item_data['seller'] = seller_name if seller_name else 'N/A'
                    except Exception as e:
                        print(f"Error extracting seller: {e}")
                        item_data['seller'] = 'N/A'

                    # Try to extract posting time
                    try:
                        import re
                        time_text = None

                        # Try CSS selectors
                        time_selectors = [
                            '[class*="time"]',
                            '[class*="Time"]',
                            '[class*="date"]',
                            '[class*="Date"]',
                            '[data-testid*="time"]',
                        ]

                        for sel in time_selectors:
                            elems = listing.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                text = elems[0].text.strip()
                                if 'ago' in text.lower() or any(x in text.lower() for x in ['hour', 'minute', 'day', 'week', 'month', 'year']):
                                    time_text = text
                                    break

                        # Fallback: search for time patterns in text
                        if not time_text and listing_text:
                            # Match patterns like "2 hours ago", "1 day ago", etc.
                            time_match = re.search(r'\d+\s*(second|minute|hour|day|week|month|year)s?\s*ago', listing_text, re.IGNORECASE)
                            if time_match:
                                time_text = time_match.group()
                            else:
                                # Look for lines containing time indicators
                                lines = [line.strip() for line in listing_text.split('\n') if line.strip()]
                                for line in lines:
                                    if 'ago' in line.lower():
                                        time_text = line
                                        break

                        item_data['time'] = time_text if time_text else 'N/A'
                    except Exception as e:
                        print(f"Error extracting time: {e}")
                        item_data['time'] = 'N/A'

                    # Try to extract condition
                    try:
                        condition_text = None

                        # Try CSS selectors
                        condition_selectors = [
                            '[class*="condition"]',
                            '[class*="Condition"]',
                            '[data-testid*="condition"]',
                        ]

                        for sel in condition_selectors:
                            elems = listing.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                text = elems[0].text.strip()
                                if text:
                                    condition_text = text
                                    break

                        # Fallback: search for condition keywords in text
                        if not condition_text and listing_text:
                            condition_keywords = [
                                'brand new', 'new', 'like new', 'lightly used',
                                'well-maintained', 'heavily used', 'mint',
                                'excellent condition', 'good condition', 'fair condition'
                            ]
                            text_lower = listing_text.lower()
                            for keyword in condition_keywords:
                                if keyword in text_lower:
                                    # Find the actual casing
                                    lines = [line.strip() for line in listing_text.split('\n') if line.strip()]
                                    for line in lines:
                                        if keyword in line.lower():
                                            condition_text = line
                                            break
                                    if condition_text:
                                        break

                        item_data['condition'] = condition_text if condition_text else 'N/A'
                    except Exception as e:
                        print(f"Error extracting condition: {e}")
                        item_data['condition'] = 'N/A'

                    # Only add if we have at least a URL or name
                    if item_data.get('url') != 'N/A' or item_data.get('name') != 'N/A':
                        results.append(item_data)
                        print(f"Extracted item {len(results)}: {item_data.get('name', 'N/A')[:50]}")
                        print(f"  Price: {item_data.get('price', 'N/A')}, Seller: {item_data.get('seller', 'N/A')}, Time: {item_data.get('time', 'N/A')}, Condition: {item_data.get('condition', 'N/A')}")

                except Exception as e:
                    print(f"Error extracting data from listing {idx}: {str(e)}")
                    continue

                # Small delay between processing items (only for larger batches)
                if max_results > 20 and idx % 10 == 0 and idx > 0:
                    time.sleep(random.uniform(0.3, 0.5))

            # Restore implicit wait
            self.driver.implicitly_wait(3)

            print(f"Successfully extracted {len(results)} items")

        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            # Restore implicit wait even on error
            if self.driver:
                self.driver.implicitly_wait(3)

        return results

    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("Browser closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def scrape_carousell(query: str, max_results: int = 20, headless: bool = True) -> List[Dict[str, str]]:
    """
    Convenience function to scrape Carousell

    Args:
        query: Search term
        max_results: Maximum number of results
        headless: Run browser in headless mode

    Returns:
        List of product dictionaries
    """
    with CarousellScraper(headless=headless) as scraper:
        return scraper.search(query, max_results)
