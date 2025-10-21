# Installation Guide - Carousell.sg Scraper

This guide will help you set up the scraper, especially on WSL2/Linux systems.

## Prerequisites

The scraper requires:
1. Python 3.8 or higher
2. A web browser (Chrome/Chromium or Firefox)
3. Required Python packages

## Step 1: Install a Web Browser

The scraper uses Selenium which requires a browser. Choose **one** of the following:

### Option A: Install Chromium (Recommended for WSL2)

```bash
sudo apt update
sudo apt install -y chromium-browser
```

Verify installation:
```bash
chromium-browser --version
```

### Option B: Install Firefox

```bash
sudo apt update
sudo apt install -y firefox
```

Verify installation:
```bash
firefox --version
```

### Option C: Install Google Chrome (Alternative)

```bash
# Download Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Chrome
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Clean up
rm google-chrome-stable_current_amd64.deb
```

Verify installation:
```bash
google-chrome --version
```

## Step 2: Install Python Dependencies

```bash
cd web-scraping

# Install dependencies
pip install -r requirements.txt
```

If you're using a virtual environment (recommended):

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Test the Installation

### Quick Test

```python
python3 -c "from src.carousell_scraper import CarousellScraper; print('Installation successful!')"
```

### Full Test

```bash
streamlit run app.py
```

Then open your browser to http://localhost:8501 and try a search.

## Troubleshooting

### Error: "No supported browser found"

**Problem**: The scraper can't find Chrome or Firefox on your system.

**Solution**: Install a browser (see Step 1 above).

### Error: "ChromeDriver unexpectedly exited. Status code was: 127"

**Problem**: Chrome is installed but missing dependencies.

**Solution**: Install required libraries:

```bash
# For Chromium on WSL2/Ubuntu
sudo apt update
sudo apt install -y chromium-browser

# Or install Chrome dependencies
sudo apt install -y libnss3 libgconf-2-4 libfontconfig1
```

### Error: "SessionNotCreatedException" or version mismatch

**Problem**: Browser and driver versions don't match.

**Solution**: The `webdriver-manager` package should handle this automatically. If issues persist:

```bash
# Clear the driver cache
rm -rf ~/.wdm

# Reinstall webdriver-manager
pip install --upgrade webdriver-manager
```

### Error: "selenium.common.exceptions.WebDriverException"

**Problem**: Display issues in headless mode on WSL2.

**Solution**: Install X virtual framebuffer:

```bash
sudo apt install -y xvfb

# Run with xvfb
xvfb-run streamlit run app.py
```

### Firefox-specific issues

If Firefox doesn't work in headless mode:

```python
# In your code, force non-headless mode
from src.carousell_scraper import scrape_carousell

results = scrape_carousell(
    query="laptop",
    headless=False  # Run with visible browser
)
```

### Slow performance on WSL2

WSL2 can be slower for GUI applications. Try:

1. **Use headless mode** (default):
   ```python
   scrape_carousell(query="laptop", headless=True)
   ```

2. **Install Chrome instead of Firefox** (usually faster on WSL2)

3. **Reduce the number of results**:
   ```python
   scrape_carousell(query="laptop", max_results=10)
   ```

## Platform-Specific Notes

### WSL2 (Windows Subsystem for Linux)

- **Chromium** is recommended over Chrome or Firefox
- **Headless mode** is recommended (no GUI needed)
- If you need to see the browser, install an X server on Windows (e.g., VcXsrv)

### Ubuntu/Debian Linux

Both Chromium and Firefox work well:

```bash
# Chromium
sudo apt install chromium-browser

# OR Firefox
sudo apt install firefox
```

### macOS

Use Homebrew:

```bash
# Chrome
brew install --cask google-chrome

# OR Firefox
brew install --cask firefox
```

Then install Python packages:
```bash
pip install -r requirements.txt
```

## Verify Everything Works

Run this test script:

```bash
cd web-scraping
python3 examples/example_usage.py
```

Select option 1 for a simple test search.

## Getting Help

If you're still having issues:

1. Check which browser is installed:
   ```bash
   which chromium-browser google-chrome firefox
   ```

2. Check Python version:
   ```bash
   python3 --version  # Should be 3.8 or higher
   ```

3. Check installed packages:
   ```bash
   pip list | grep -E 'selenium|webdriver|streamlit'
   ```

4. Run with verbose error messages:
   ```python
   from src.carousell_scraper import CarousellScraper

   try:
       with CarousellScraper(headless=True) as scraper:
           results = scraper.search("test", max_results=5)
           print(f"Success! Found {len(results)} results")
   except Exception as e:
       print(f"Error: {e}")
       import traceback
       traceback.print_exc()
   ```

## Next Steps

Once everything is installed:

1. Read the [Quick Start Guide](QUICKSTART.md)
2. Try the [Example Scripts](examples/example_usage.py)
3. Check the [Full Documentation](CAROUSELL_README.md)

---

**Need more help?** Check the error message carefully - it usually indicates what's missing!
