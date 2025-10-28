"""
Wrapper script for the Streamlit app with error handling
This keeps the console window open on errors
"""
import sys
import os
import traceback
from pathlib import Path

def main():
    try:
        # Get the directory where the script is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            application_path = Path(sys._MEIPASS)
        else:
            # Running as normal Python script
            application_path = Path(__file__).parent

        # Change to application directory
        os.chdir(application_path)

        # Add src to path
        sys.path.insert(0, str(application_path / 'src'))

        # Set Streamlit config directory
        streamlit_config_dir = application_path / '.streamlit'
        if streamlit_config_dir.exists():
            os.environ['STREAMLIT_CONFIG_DIR'] = str(streamlit_config_dir)

        print("=" * 60)
        print("Carousell Scraper - Starting...")
        print("=" * 60)
        print(f"Application path: {application_path}")
        print(f"Current directory: {os.getcwd()}")
        print()

        # Set Streamlit config
        os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

        # Check if Chrome is available
        import shutil
        chrome_paths = [
            'google-chrome', 'chrome', 'chromium', 'chromium-browser',
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ]

        chrome_found = False
        for chrome_path in chrome_paths:
            if shutil.which(chrome_path) or Path(chrome_path).exists():
                print(f"✓ Found Chrome: {chrome_path}")
                chrome_found = True
                break

        if not chrome_found:
            print("⚠ WARNING: Chrome not detected. Please install Google Chrome.")
            print("   Download from: https://www.google.com/chrome/")
            print()

        # Import and run streamlit
        print("Starting Streamlit server...")
        print("Please wait, this may take 30-60 seconds on first run...")
        print()

        from streamlit.web import cli as stcli

        # Run the Streamlit app
        sys.argv = [
            "streamlit",
            "run",
            str(application_path / "app.py"),
            "--server.headless=true",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.serverAddress=localhost",
            "--browser.gatherUsageStats=false",
            "--global.developmentMode=false",
        ]

        print("Streamlit should open in your browser at: http://localhost:8501")
        print("If it doesn't open automatically, copy and paste the URL above.")
        print()

        sys.exit(stcli.main())

    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR OCCURRED!")
        print("=" * 60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print()
        print("Full traceback:")
        print("-" * 60)
        traceback.print_exc()
        print("-" * 60)
        print()
        print("Common solutions:")
        print("1. Make sure Google Chrome is installed")
        print("2. Check your internet connection")
        print("3. Try running as administrator")
        print("4. Check Windows Defender/antivirus isn't blocking")
        print()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()
