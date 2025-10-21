# Carousell.sg Web Scraper

A robust web scraper for Carousell.sg with a user-friendly Streamlit interface.

## Features

- **Streamlit Web Interface**: Easy-to-use GUI for searching and viewing results
- **Selenium-based Scraping**: Handles JavaScript-rendered content
- **Safety Features**:
  - Random delays between requests (2-5 seconds)
  - Human-like scrolling behavior
  - Proper browser headers to avoid detection
  - Rate limiting to prevent server overload
- **Data Extraction**:
  - Item names
  - Prices
  - Product URLs/links
- **Export Functionality**: Download results as CSV

## Installation

1. **Navigate to the web-scraping directory**:
   ```bash
   cd web-scraping
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Chrome/Chromium** (if not already installed):
   - The scraper uses Chrome via Selenium
   - WebDriver Manager will automatically download the appropriate ChromeDriver

## Usage

### Option 1: Streamlit Web Interface (Recommended)

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to the URL shown (usually http://localhost:8501)

3. **Enter your search term** and click "Start Scraping"

4. **View and download results** as a table or CSV file

### Option 2: Python Script

Create a Python script to use the scraper programmatically:

```python
from src.carousell_scraper import scrape_carousell

# Scrape for laptops
results = scrape_carousell(
    query="laptop",
    max_results=20,
    headless=True
)

# Print results
for item in results:
    print(f"Name: {item['name']}")
    print(f"Price: {item['price']}")
    print(f"URL: {item['url']}")
    print("-" * 50)
```

### Option 3: Using the CarousellScraper Class

For more control, use the scraper class directly:

```python
from src.carousell_scraper import CarousellScraper

# Use as context manager
with CarousellScraper(headless=True, delay_range=(3, 6)) as scraper:
    results = scraper.search("iPhone", max_results=30)

    # Process results
    for item in results:
        print(item)
```

## Configuration

### Scraper Options

- **headless**: Run browser without GUI (default: True)
- **delay_range**: Tuple of (min, max) seconds for random delays (default: (2, 5))
- **max_results**: Maximum number of items to scrape (default: 20)

### Example with Custom Settings

```python
from src.carousell_scraper import CarousellScraper

scraper = CarousellScraper(
    headless=False,  # Show browser window
    delay_range=(3, 7)  # Longer delays for extra safety
)

results = scraper.search("furniture", max_results=50)
scraper.close()
```

## Safety and Best Practices

### Built-in Safety Features

1. **Random Delays**: The scraper adds 2-5 second delays between requests
2. **Human-like Behavior**: Implements scrolling and mouse movements
3. **Rate Limiting**: Processes items in batches with pauses
4. **Proper Headers**: Uses realistic browser user-agent strings

### Recommendations

- ⚠️ **Respect Terms of Service**: Always check and comply with Carousell's ToS
- 🕐 **Limit Frequency**: Don't scrape too frequently
- 📊 **Cache Results**: Store results locally to avoid repeated scraping
- 🤝 **Be Ethical**: Only scrape publicly available data
- 🚫 **Avoid Peak Hours**: Scrape during off-peak times if possible

## Troubleshooting

### Chrome/ChromeDriver Issues

If you encounter Chrome or ChromeDriver errors:

```bash
# Update webdriver-manager cache
pip install --upgrade webdriver-manager

# Or manually specify Chrome binary location
chrome_options.binary_location = "/path/to/chrome"
```

### 403 Forbidden Errors

If you get 403 errors:
- The site may have updated its anti-bot measures
- Try increasing delay_range to (5, 10)
- Run with headless=False to see what's happening
- Check if the site structure has changed

### No Results Found

If scraping returns empty results:
- The HTML structure may have changed
- Try running with headless=False to inspect the page
- Check the browser console for errors
- Update the CSS selectors in [carousell_scraper.py](src/carousell_scraper.py)

### Selenium Timeout

If you get timeout errors:
- Increase the timeout value in WebDriverWait
- Check your internet connection
- Try running with headless=False to see page loading

## Output Format

The scraper returns a list of dictionaries with the following structure:

```python
[
    {
        'name': 'Gaming Laptop - ASUS ROG',
        'price': 'S$ 1,200',
        'url': 'https://www.carousell.sg/p/...'
    },
    {
        'name': 'MacBook Pro 2020',
        'price': 'S$ 1,800',
        'url': 'https://www.carousell.sg/p/...'
    }
]
```

## Project Structure

```
web-scraping/
├── app.py                      # Streamlit frontend
├── src/
│   ├── __init__.py
│   └── carousell_scraper.py   # Main scraper module
├── requirements.txt            # Python dependencies
├── CAROUSELL_README.md        # This file
└── examples/
    └── example_usage.py       # Example scripts
```

## Dependencies

- **selenium**: Web browser automation
- **webdriver-manager**: Automatic ChromeDriver management
- **streamlit**: Web interface
- **pandas**: Data processing and export

## Legal and Ethical Considerations

This tool is provided for educational purposes only. Users are responsible for:

1. Complying with Carousell's Terms of Service
2. Respecting robots.txt directives
3. Not overloading the server with requests
4. Using the data ethically and legally
5. Respecting privacy and data protection laws

## Contributing

Feel free to improve the scraper by:
- Adding more robust selectors
- Implementing pagination
- Adding more safety features
- Improving error handling

## License

This project is for educational purposes. Use responsibly and at your own risk.

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify your Chrome and ChromeDriver versions
3. Ensure all dependencies are installed correctly
4. Check if Carousell's HTML structure has changed

---

**Note**: Web scraping should always be done responsibly and ethically. Always respect the website's terms of service and rate limits.
