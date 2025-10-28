# Troubleshooting Guide

## Issue: "This site can't be reached" or "Connection refused"

### Symptoms:
- Exe runs and shows "You can now view your Streamlit app in your browser"
- Shows URLs like http://localhost:3000 or http://192.168.x.x:3000
- Browser can't connect - shows "refused to connect" error

### Root Cause:
Streamlit is using the wrong port or address configuration.

### Solution:

**Option 1: Use the correct URL (Quick Fix)**

The app should be available at: **http://localhost:8501**

Try this URL in your browser even if the console shows a different port.

**Option 2: Rebuild with fixed configuration (Permanent Fix)**

```powershell
cd E:\git\web-scraping
git pull  # Get the latest fixes

# Clean rebuild
Remove-Item -Recurse -Force build, dist
pyinstaller build_exe.spec --clean

# Run it
cd dist
.\CarousellScraper.exe
```

The new build includes:
- ✅ Fixed port to 8501
- ✅ Streamlit config file (.streamlit/config.toml)
- ✅ Explicit localhost binding
- ✅ Disabled CORS that can cause issues

---

## Issue: Port 8501 is already in use

### Symptoms:
- Error: "Address already in use"
- Can't start Streamlit server

### Solution:

**Kill existing Streamlit processes:**

```powershell
# Find processes using port 8501
netstat -ano | findstr :8501

# Kill the process (replace XXXX with PID from above)
taskkill /PID XXXX /F

# Or kill all Python processes:
taskkill /F /IM python.exe
taskkill /F /IM CarousellScraper.exe
```

---

## Issue: Browser doesn't open automatically

### Solution:

Manually open your browser and go to: **http://localhost:8501**

The server is running, just the auto-open feature failed.

---

## Issue: Firewall blocking the connection

### Symptoms:
- Console shows server started
- Browser can't connect
- No error in console

### Solution:

**Allow through Windows Firewall:**

```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "Carousell Scraper" -Direction Inbound -Program "E:\git\web-scraping\dist\CarousellScraper.exe" -Action Allow
```

Or manually:
1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Browse to CarousellScraper.exe
4. Check both Private and Public networks
5. Click OK

---

## Issue: Streamlit page loads but is blank/spinning

### Symptoms:
- Browser connects successfully
- Page shows Streamlit header but content doesn't load
- Infinite loading spinner

### Solution:

**Check console for JavaScript errors:**

1. Press F12 in browser
2. Go to Console tab
3. Look for errors about missing static files

**If you see "404 Not Found" for static files:**

The build didn't include Streamlit's web assets properly.

```powershell
# Verify Streamlit is installed in venv
venv\Scripts\activate
python -c "import streamlit; print(streamlit.__version__)"

# Should print version without errors
# If error, reinstall:
pip install --force-reinstall streamlit

# Then rebuild
pyinstaller build_exe.spec --clean
```

---

## Issue: Different port (3000, 8080, etc.) shown instead of 8501

### Cause:
Streamlit detected port 8501 was busy and auto-selected another port.

### Solution:

**Option 1:** Use whatever port is shown (if it works)

**Option 2:** Make sure no other apps are using port 8501:

```powershell
# Check what's using port 8501
netstat -ano | findstr :8501

# If something is using it, kill it:
taskkill /PID <PID> /F

# Common culprits:
# - Old Streamlit instances
# - Other web servers (Node.js, Python)
# - Docker containers
```

---

## Issue: "ModuleNotFoundError" when running exe

### Symptoms:
- Console shows missing module error
- Typically: streamlit.web.cli, tornado, click, etc.

### Solution:

**Rebuild with updated spec file:**

The latest `build_exe.spec` includes all necessary hidden imports.

```powershell
git pull
pip install --upgrade streamlit tornado click altair watchdog validators
pyinstaller build_exe.spec --clean
```

---

## Issue: Chrome opens but shows "localhost refused to connect"

### This means Streamlit server isn't actually running.

**Check console for errors:**

Look in the console window for:
- Python tracebacks
- Import errors
- Port binding errors

**Common causes:**

1. **Missing dependencies:** Rebuild with all deps installed
2. **Antivirus blocking:** Add exe to exclusions
3. **Python environment issues:** Use clean venv

**Debug steps:**

```powershell
# Test the app WITHOUT PyInstaller first:
cd E:\git\web-scraping
venv\Scripts\activate
streamlit run app.py

# If this works, PyInstaller should work too
# If this fails, fix the app first before building exe
```

---

## Issue: Network URL shows external IP instead of localhost

### This is normal!

Streamlit shows three URLs:
- **Local URL:** For your machine only (http://localhost:8501)
- **Network URL:** For other devices on your network
- **External URL:** For internet access (usually blocked by router)

**Use Local URL** for best reliability: http://localhost:8501

---

## Issue: Works on build machine but not on other computers

### Common causes:

1. **Chrome not installed** on target machine
   - Solution: Install Chrome

2. **Missing Visual C++ Redistributable**
   - Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
   - Install on target machine

3. **Antivirus blocking exe**
   - Add to exclusions or whitelist

4. **Different Windows version**
   - Build on Windows 10 if targeting Windows 10
   - Build on Windows 11 if targeting Windows 11

---

## Still having issues?

### Debug mode:

Run the exe from PowerShell to see all output:

```powershell
cd E:\git\web-scraping\dist
.\CarousellScraper.exe
```

Keep the console window open and watch for:
- Error messages
- Which port it's trying to use
- Whether Chrome is detected
- Any Python tracebacks

### Capture logs:

```powershell
.\CarousellScraper.exe > log.txt 2>&1
# Then share log.txt for help
```

### Test without packaging:

```powershell
# Go back to source
cd E:\git\web-scraping
venv\Scripts\activate

# Run directly
streamlit run app.py

# If this works, the problem is with PyInstaller packaging
# If this fails, the problem is with the app itself
```
