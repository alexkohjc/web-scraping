# WSL2 Setup Guide

## What Those Errors Mean

The errors you're seeing are **NORMAL for WSL2**:

```
/usr/bin/x-www-browser: 12: xdg-settings: not found
WARNING: cannot start document portal
```

These happen because WSL2 doesn't have a GUI display by default. **This is not a problem** - we'll work around it!

## Complete Setup for WSL2

### Step 1: Install Firefox (for headless scraping)

Firefox will run in headless mode (no GUI needed):

```bash
sudo apt update
sudo apt install -y firefox
```

### Step 2: Access Streamlit from Windows Browser

Since WSL2 can't open GUI apps, you'll access Streamlit from your Windows browser.

**Run Streamlit:**
```bash
cd web-scraping
streamlit run app.py
```

**What you'll see:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.x.x.x:8501
```

**Ignore the errors** - they're harmless!

**Open in Windows:**
1. Look for the line that says `Local URL: http://localhost:8501`
2. Copy that URL
3. Open your **Windows browser** (Chrome, Edge, Firefox on Windows)
4. Paste the URL: `http://localhost:8501`

That's it! The Streamlit interface will appear in your Windows browser.

---

## Alternative: Use Python Script (No Browser Needed)

If you prefer to avoid Streamlit entirely, use the scraper directly:

### Create a simple script:

```bash
cd web-scraping
cat > test_scraper.py << 'EOF'
from src.carousell_scraper import scrape_carousell
import pandas as pd

# Search for laptops
print("Searching for laptops on Carousell.sg...")
results = scrape_carousell(
    query="laptop",
    max_results=10,
    headless=True  # No GUI needed
)

# Display results
if results:
    df = pd.DataFrame(results)
    print(f"\nFound {len(results)} results:\n")
    print(df.to_string())

    # Save to CSV
    df.to_csv("results.csv", index=False)
    print(f"\nSaved to results.csv")
else:
    print("No results found")
EOF
```

### Run it:

```bash
python3 test_scraper.py
```

This will:
- Search Carousell.sg
- Print results to terminal
- Save results to `results.csv`
- **No browser window needed!**

---

## Understanding Headless Mode

**Headless mode** means:
- ✅ Browser runs in the background (no GUI)
- ✅ Perfect for WSL2
- ✅ Faster and uses less resources
- ❌ You won't see the browser window (but you don't need to!)

The scraper is **designed for headless mode** on WSL2!

---

## Quick Commands Reference

### Option 1: Use Streamlit (Recommended)

```bash
cd web-scraping
streamlit run app.py
# Then open http://localhost:8501 in Windows browser
```

### Option 2: Use Python Script

```bash
cd web-scraping
python3 test_scraper.py
```

### Option 3: Use Interactive Examples

```bash
cd web-scraping
python3 examples/example_usage.py
```

---

## Troubleshooting

### "No browser found" error

Install Firefox:
```bash
sudo apt update && sudo apt install -y firefox
```

### Streamlit won't open

1. Don't worry about the xdg-settings errors - they're harmless
2. Just open `http://localhost:8501` in your **Windows browser**
3. Make sure Streamlit is running (you should see "You can now view your Streamlit app")

### Can't access localhost:8501 from Windows

Try the Network URL instead:
```bash
# Look for this in the Streamlit output:
Network URL: http://172.x.x.x:8501

# Use that IP in Windows browser
```

Or configure Windows firewall to allow WSL2 connections.

### Firefox installation fails

Try Chromium + dependencies:
```bash
sudo apt update
sudo apt install -y chromium-browser libnss3 libnspr4
```

---

## Why This Setup Works

1. **Firefox runs headless** in WSL2 (no display needed)
2. **Scraper runs in WSL2** using headless Firefox
3. **Streamlit web server** runs in WSL2
4. **You access Streamlit** from Windows browser via localhost
5. **Results display** in Windows browser

Everyone's happy! 🎉

---

## Next Steps

1. ✅ Install Firefox: `sudo apt install -y firefox`
2. ✅ Run Streamlit: `streamlit run app.py`
3. ✅ Open in Windows browser: `http://localhost:8501`
4. ✅ Start scraping!

---

**Pro Tip**: The errors you saw are cosmetic. As long as you can access `http://localhost:8501` from Windows, everything works perfectly!
