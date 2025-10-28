# Building Carousell Scraper as Windows Executable

This guide explains how to package the Streamlit web scraper as a standalone `.exe` file for Windows.

## Prerequisites

### On the Target Windows Machine:
1. **Python 3.8+** (only needed for building, not for running the final .exe)
2. **Google Chrome** or **Chromium** browser installed
3. Git (optional, for cloning the project)

## Step-by-Step Build Instructions

### 1. Transfer Project to Windows Machine

**Option A: Using Git**
```bash
git clone <your-repo-url>
cd web-scraping
```

**Option B: Manual Copy**
- Copy the entire `web-scraping` folder to the Windows machine
- Make sure all files are included: `app.py`, `src/`, `requirements.txt`, etc.

### 2. Install Python Dependencies

Open PowerShell or Command Prompt in the project folder:

```bash
# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller
```

### 3. Build the Executable

Run PyInstaller with the provided spec file:

```bash
pyinstaller build_exe.spec
```

This will:
- Create a `dist/` folder
- Generate `CarousellScraper.exe` inside the `dist/` folder
- Take 5-10 minutes depending on your machine
- Result in a ~300-500MB executable (includes Python + all dependencies)

### 4. Test the Executable

```bash
cd dist
.\CarousellScraper.exe
```

The application should:
1. Open a console window
2. Start the Streamlit server
3. Automatically open your default browser to the app
4. Display the Carousell scraper interface

### 5. Distribution

To share with another user:

1. Copy the entire `dist/CarousellScraper.exe` file
2. Send it to the user
3. User must have **Chrome or Chromium** installed
4. User double-clicks `CarousellScraper.exe` to run

## Alternative: One-Folder Distribution

If you prefer a folder with multiple files (faster startup):

```bash
pyinstaller build_exe_folder.spec
```

This creates a `dist/CarousellScraper/` folder with:
- `CarousellScraper.exe`
- Supporting DLL files and libraries
- Smaller exe file but requires the whole folder

## Common Issues & Solutions

### Issue 1: "Chrome binary not found"
**Solution**: Install Google Chrome or Chromium on the target machine
- Download from: https://www.google.com/chrome/

### Issue 2: Executable is too large
**Solution**: Use the one-folder distribution or consider:
```bash
# Build with UPX compression (requires UPX installed)
pyinstaller build_exe.spec --upx-dir=<path-to-upx>
```

### Issue 3: Antivirus flags the .exe
**Solution**: This is common with PyInstaller executables
- Add exception to Windows Defender
- Build on a clean Windows machine
- Code-sign the executable (requires certificate)

### Issue 4: Streamlit port already in use
**Solution**: The app will automatically try different ports. If it fails:
```bash
# Run with specific port
CarousellScraper.exe -- --server.port 8502
```

### Issue 5: "DLL load failed"
**Solution**: Install Microsoft Visual C++ Redistributable
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

## Advanced: Building Without Python on Windows

If you don't have access to a Windows machine, you can:

1. **Use GitHub Actions** (recommended for CI/CD)
2. **Use a Windows VM** (VirtualBox, VMware)
3. **Use Wine on Linux** (limited support, not recommended)

## File Structure After Build

```
web-scraping/
├── app.py
├── src/
│   └── carousell_scraper.py
├── requirements.txt
├── build_exe.spec
├── build/                  # Temporary build files
│   └── ...
└── dist/                   # Output folder
    └── CarousellScraper.exe  (or CarousellScraper/ folder)
```

## Security Note

The executable contains your source code in a semi-compiled form. While not easily readable, it can be decompiled. If you have sensitive information:
- Store API keys in environment variables
- Don't hardcode credentials
- Consider using a license/authentication system

## Performance Note

- **First Run**: May take 30-60 seconds to start (extracting libraries)
- **Subsequent Runs**: Faster, ~10-20 seconds
- **File Size**: 300-500MB (can't be reduced much due to dependencies)

## User Guide for End Users

### Running the Application

1. **Download** `CarousellScraper.exe`
2. **Important**: Make sure Google Chrome is installed
3. **Double-click** `CarousellScraper.exe`
4. **Wait** for console window to appear (may take 30-60 seconds on first run)
5. **Browser will open** automatically showing the scraper interface
6. **Enter search term** and click "Start Scraping"
7. **Keep "Headless Mode" unchecked** for best results (recommended)
8. **Wait** for results (browser window will appear)
9. **Download results** as CSV if needed

### System Requirements

- Windows 10/11 (64-bit)
- Google Chrome or Chromium browser
- 4GB RAM minimum
- Internet connection

### Troubleshooting for Users

**Q: Nothing happens when I double-click**
- A: Wait 30-60 seconds, it's loading Python and libraries

**Q: Browser doesn't open**
- A: Check console window for URL (usually http://localhost:8501)
- A: Manually open that URL in Chrome

**Q: "Chrome binary not found" error**
- A: Install Google Chrome from https://www.google.com/chrome/

**Q: Windows Defender blocks the file**
- A: Click "More info" → "Run anyway" (the file is safe)
