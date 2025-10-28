"""
Launcher script for the Streamlit app when running as executable
This helps handle paths correctly when bundled with PyInstaller
"""
import sys
import os
from pathlib import Path

def main():
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

    # Set Streamlit config to automatically open browser
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

    # Import and run streamlit
    from streamlit.web import cli as stcli

    # Run the Streamlit app
    sys.argv = [
        "streamlit",
        "run",
        str(application_path / "app.py"),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    sys.exit(stcli.main())

if __name__ == '__main__':
    main()
