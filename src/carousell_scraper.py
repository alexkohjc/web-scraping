"""
Carousell.sg Web Scraper
Scrapes product listings from Carousell.sg search results
"""

import time
import random
import shutil
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
        try:
            from selenium.webdriver.chrome.options import Options

            print("Setting up Chrome driver...")
            chrome_options = Options()

            if self.headless:
                chrome_options.add_argument("--headless=new")

            # Add options to make the browser appear more human-like
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            # WSL2 and headless-specific fixes for DevToolsActivePort error
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-setuid-sandbox")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-background-networking")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--metrics-recording-only")
            chrome_options.add_argument("--mute-audio")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--safebrowsing-disable-auto-update")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--ignore-ssl-errors")

            # Set page load strategy to 'eager' for faster loading
            # 'eager' waits for DOM ready, not all resources (images, stylesheets)
            chrome_options.page_load_strategy = 'eager'

            # Disable automation flags
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Use Selenium Manager (built into Selenium 4.6+) to automatically manage ChromeDriver
            # Selenium Manager will automatically download the correct ChromeDriver version for Chrome 141
            print("Using Selenium Manager to auto-download matching ChromeDriver...")
            self.driver = webdriver.Chrome(options=chrome_options)

            # Set timeouts to prevent hanging
            self.driver.set_page_load_timeout(30)  # 30 second page load timeout
            self.driver.implicitly_wait(3)  # Reduced to 3 seconds for faster performance

            # Execute script to hide webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        except Exception as e:
            raise RuntimeError(f"Failed to setup Chrome driver: {e}\nTry installing Firefox instead.")

    def _setup_firefox(self):
        """Setup Firefox driver"""
        try:
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.firefox.service import Service
            from webdriver_manager.firefox import GeckoDriverManager

            print("Setting up Firefox driver...")
            firefox_options = Options()

            if self.headless:
                firefox_options.add_argument("--headless")

            # Add options to make the browser appear more human-like
            firefox_options.set_preference("dom.webdriver.enabled", False)
            firefox_options.set_preference('useAutomationExtension', False)
            firefox_options.set_preference("general.useragent.override",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0")

            # Setup driver with webdriver_manager
            service = Service(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=firefox_options)

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
                    screenshot_path = "debug_screenshot.png"
                    self.driver.save_screenshot(screenshot_path)
                    print(f"Saved debug screenshot to: {screenshot_path}")
                except:
                    pass
                return results

            print(f"Processing {min(len(all_listings), max_results)} listings...")

            # Temporarily disable implicit wait for faster extraction
            self.driver.implicitly_wait(0)


            # Extract information from each listing
            for idx, listing in enumerate(all_listings[:max_results]):
                try:
                    item_data = {}

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

                    # Try to extract the title/name
                    try:
                        # Try multiple selectors for title (using find_elements for speed)
                        title_selectors = ['h3', 'h4', 'p[class*="title"]', '[class*="Title"]', '[data-testid*="title"]']
                        title_text = None
                        for sel in title_selectors:
                            elems = listing.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                title_text = elems[0].text.strip()
                                if title_text:
                                    break

                        if not title_text and listing.text:
                            # Fallback: use the first line of text
                            title_text = listing.text.split('\n')[0]

                        item_data['name'] = title_text if title_text else 'N/A'
                    except:
                        item_data['name'] = 'N/A'

                    # Try to extract the price
                    try:
                        # Look for price with $ symbol (using find_elements for speed)
                        price_selectors = [
                            '[class*="price"]',
                            '[data-testid*="price"]',
                        ]
                        price_text = None

                        for sel in price_selectors:
                            elems = listing.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                price_text = elems[0].text.strip()
                                if price_text and '$' in price_text:
                                    break

                        # Fallback: search in all text for price pattern
                        if not price_text:
                            import re
                            text = listing.text
                            price_match = re.search(r'S?\$\s*[\d,]+(?:\.\d{2})?', text)
                            if price_match:
                                price_text = price_match.group()

                        item_data['price'] = price_text if price_text else 'N/A'
                    except:
                        item_data['price'] = 'N/A'

                    # Only add if we have at least a URL or name
                    if item_data.get('url') != 'N/A' or item_data.get('name') != 'N/A':
                        results.append(item_data)
                        print(f"Extracted item {len(results)}: {item_data.get('name', 'N/A')[:50]}")

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
