# Fix: ChromeDriver Status Code 127

## What's Wrong?

You're getting this error:
```
Service /home/alex/.wdm/drivers/chromedriver/linux64/114.0.5735.90/chromedriver
unexpectedly exited. Status code was: 127
```

**Cause**: ChromeDriver is missing required NSS (Network Security Services) libraries.

## Quick Fix - Choose One Option

### ⭐ Option 1: Install Firefox (EASIEST - Recommended for WSL2)

Firefox works better on WSL2 and has fewer dependencies:

```bash
sudo apt update && sudo apt install -y firefox
```

Then test:
```bash
cd web-scraping
streamlit run app.py
```

The scraper will automatically detect and use Firefox!

---

### Option 2: Fix Chrome/Chromium (Install Missing Libraries)

Install the missing NSS libraries:

```bash
sudo apt update
sudo apt install -y libnss3 libnss3-dev libnspr4 libnspr4-dev
```

Then test:
```bash
cd web-scraping
streamlit run app.py
```

---

## Verify the Fix

Run the diagnostic script to check everything:

```bash
cd web-scraping
python3 diagnose.py
```

This will:
- Check which browsers are installed
- Verify all dependencies
- Test if Selenium can actually start the browser
- Give you specific recommendations

## Expected Output After Fix

✓ You should see:
```
✓ Successfully started Firefox!
```
or
```
✓ Successfully started Chrome!
```

## Still Having Issues?

### Check what's installed:
```bash
# Check for browsers
which firefox chromium-browser google-chrome

# Check for NSS libraries (for Chrome)
ldconfig -p | grep libnss3
```

### Try each browser manually:

**Test Chrome:**
```python
cd web-scraping
python3 -c "
from src.carousell_scraper import CarousellScraper
scraper = CarousellScraper(browser='chrome', headless=True)
scraper._setup_driver()
print('Chrome works!')
scraper.close()
"
```

**Test Firefox:**
```python
cd web-scraping
python3 -c "
from src.carousell_scraper import CarousellScraper
scraper = CarousellScraper(browser='firefox', headless=True)
scraper._setup_driver()
print('Firefox works!')
scraper.close()
"
```

## Why Firefox is Recommended for WSL2

- ✅ Fewer dependencies
- ✅ Works better in headless mode on WSL2
- ✅ More reliable on Linux
- ✅ Easier to install

## Complete Clean Install (Nuclear Option)

If nothing works, start fresh:

```bash
# 1. Remove old drivers
rm -rf ~/.wdm

# 2. Uninstall browsers
sudo apt remove chromium-browser google-chrome firefox

# 3. Install Firefox fresh
sudo apt update
sudo apt install -y firefox

# 4. Reinstall Python packages
cd web-scraping
pip install --upgrade --force-reinstall selenium webdriver-manager

# 5. Test
python3 diagnose.py
```

## Next Steps

Once your browser is working:

1. ✅ Run `streamlit run app.py`
2. ✅ Try searching for "laptop" or any term
3. ✅ Check the results

---

**Need more help?** Run `python3 diagnose.py` and share the output!
