# Quick Build Guide for Windows

## ✅ What I Fixed

The `importlib.metadata.PackageNotFoundError` error you saw is a known issue with Streamlit and PyInstaller. I've added:

1. **Runtime hook** (`fix_streamlit_hook.py`) - Patches Streamlit's version detection
2. **Additional hidden imports** - Ensures all Streamlit modules are included
3. **Static file collection** - Includes Streamlit's web UI files
4. **Error wrapper** (`app_wrapper.py`) - Better error messages and diagnostics

## 🚀 Build Instructions

### Step 1: Pull the Latest Changes

```powershell
cd E:\git\web-scraping
git pull
```

### Step 2: Clean Previous Build (Important!)

```powershell
# Remove old build artifacts
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
```

### Step 3: Activate Virtual Environment

```powershell
# If venv doesn't exist yet:
python -m venv venv

# Activate it:
venv\Scripts\activate

# You should see (venv) in your prompt
```

### Step 4: Install/Update Dependencies

```powershell
# Make sure all dependencies are up to date
pip install --upgrade -r requirements.txt
pip install --upgrade pyinstaller
```

### Step 5: Build the Executable

```powershell
# Build with the fixed spec file
pyinstaller build_exe.spec --clean

# This will take 5-10 minutes
# You'll see a lot of output - that's normal
```

### Step 6: Test the Executable

```powershell
cd dist
.\CarousellScraper.exe
```

**Expected behavior:**
1. Console window opens with startup messages
2. Shows "Starting Streamlit server..."
3. Browser automatically opens to http://localhost:8501
4. Streamlit interface appears

## 🐛 Troubleshooting

### Issue: Same metadata error

**Solution:** Make sure you did `--clean` and removed old build folders:
```powershell
Remove-Item -Recurse -Force build, dist
pyinstaller build_exe.spec --clean
```

### Issue: "Chrome not found" warning

**Solution:** Install Google Chrome:
- Download: https://www.google.com/chrome/

### Issue: Streamlit page is blank

**Solution:** Check console for errors. The static files might not be included:
```powershell
# Run the helper to verify Streamlit installation:
python collect_streamlit_data.py
```

### Issue: "Module not found" errors

**Solution:** Reinstall dependencies in the virtual environment:
```powershell
venv\Scripts\activate
pip install --upgrade -r requirements.txt
```

### Issue: Build fails with "ImportError"

**Solution:** Make sure you're in the virtual environment:
```powershell
# Check if (venv) appears in your prompt
# If not:
venv\Scripts\activate

# Verify Python is from venv:
Get-Command python
# Should show: ...\venv\Scripts\python.exe
```

## 📊 Build Output Size

- **Executable size:** ~50-80MB (compressed)
- **Unpacked size:** ~300-500MB (in memory)
- **Build time:** 5-10 minutes
- **First run time:** 30-60 seconds

## ✨ Testing Checklist

After building, test these features:

- [ ] Executable starts without errors
- [ ] Browser opens automatically
- [ ] Streamlit interface loads properly
- [ ] Can enter search term
- [ ] Scraping works (with Chrome visible)
- [ ] Results display correctly
- [ ] Can download CSV
- [ ] Console shows proper error messages if something fails

## 📦 Distribution

Once tested successfully:

1. **File to share:** `E:\git\web-scraping\dist\CarousellScraper.exe`
2. **Size:** ~50-80MB (single file)
3. **Requirements for end user:**
   - Windows 10/11 (64-bit)
   - Google Chrome installed
   - No Python needed!

### Optional: Create a distributable package

```powershell
# Create a zip file with the exe and instructions
Compress-Archive -Path dist\CarousellScraper.exe, README_DEPLOYMENT.md -DestinationPath CarousellScraper_v1.0.zip
```

## 🔧 Advanced Options

### Reduce file size (experimental)

Try UPX compression:
```powershell
# Download UPX from: https://upx.github.io/
# Then:
pyinstaller build_exe.spec --clean --upx-dir="C:\path\to\upx"
```

### Debug mode (verbose output)

```powershell
pyinstaller build_exe.spec --clean --debug=all
```

### One-folder distribution (faster startup)

```powershell
pyinstaller build_exe_folder.spec --clean
# Output: dist\CarousellScraper\ folder with multiple files
# User runs: dist\CarousellScraper\CarousellScraper.exe
```

## 🆘 Still Having Issues?

If the build still fails:

1. **Check Python version:**
   ```powershell
   python --version
   # Should be 3.8 or higher
   ```

2. **Verify Streamlit installation:**
   ```powershell
   python -c "import streamlit; print(streamlit.__version__)"
   # Should print version without errors
   ```

3. **Test the app directly (without PyInstaller):**
   ```powershell
   streamlit run app.py
   # If this works, PyInstaller should work too
   ```

4. **Check for antivirus interference:**
   - Temporarily disable Windows Defender
   - Add exclusion for the web-scraping folder

5. **Try in a fresh virtual environment:**
   ```powershell
   Remove-Item -Recurse -Force venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   pip install pyinstaller
   pyinstaller build_exe.spec --clean
   ```

## 📝 Notes

- The `fix_streamlit_hook.py` runs automatically when the exe starts
- The `app_wrapper.py` provides better error handling
- Build must be done on Windows (can't cross-compile from Linux)
- Each build is specific to the OS it was built on (Windows .exe won't run on Mac/Linux)

Good luck! 🎉
