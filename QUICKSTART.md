# Quick Start Guide - Carousell.sg Scraper

## Installation

```bash
# 1. Navigate to the project directory
cd web-scraping

# 2. Install dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: Streamlit Web App (Easiest)

```bash
streamlit run app.py
```

Then open your browser to http://localhost:8501

### Option 2: Python Script

```python
from src.carousell_scraper import scrape_carousell

# Search for items
results = scrape_carousell(query="laptop", max_results=20)

# Print results
for item in results:
    print(f"{item['name']} - {item['price']}")
    print(f"Link: {item['url']}\n")
```

### Option 3: Run Examples

```bash
cd examples
python example_usage.py
```

## What Gets Scraped

- **Item Name**: Product title
- **Price**: Listed price (in SGD)
- **URL**: Direct link to the listing

## Safety Features

- Random delays (2-5 seconds) between requests
- Human-like scrolling behavior
- Proper browser headers
- Rate limiting

## Tips

- Start with fewer results (10-20) to test
- Use headless mode for faster scraping
- Be patient - scraping takes time
- Respect the website's ToS

## Troubleshooting

**No results?**
- Check your internet connection
- Try with headless=False to see the browser
- The site structure may have changed

**Chrome errors?**
- Make sure Chrome is installed
- Run: `pip install --upgrade webdriver-manager`

---

For detailed documentation, see [CAROUSELL_README.md](CAROUSELL_README.md)
