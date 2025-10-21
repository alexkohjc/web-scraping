#!/usr/bin/env python3
"""
System Check Script for Carousell Scraper
Checks if all required dependencies and browsers are installed
"""

import sys
import shutil
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    print("=" * 70)
    print("Checking Python Version...")
    print("=" * 70)

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Python version: {version_str}")

    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version is compatible (3.8+)")
        return True
    else:
        print("✗ Python version is too old. Need 3.8 or higher.")
        return False


def check_browsers():
    """Check which browsers are installed"""
    print("\n" + "=" * 70)
    print("Checking for Browsers...")
    print("=" * 70)

    browsers = {
        'Chrome': ['google-chrome', 'chrome'],
        'Chromium': ['chromium-browser', 'chromium'],
        'Firefox': ['firefox'],
    }

    found_browsers = []

    for browser_name, commands in browsers.items():
        for cmd in commands:
            path = shutil.which(cmd)
            if path:
                # Try to get version
                try:
                    result = subprocess.run(
                        [cmd, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    version = result.stdout.strip()
                    print(f"✓ {browser_name} found: {path}")
                    print(f"  Version: {version}")
                    found_browsers.append(browser_name)
                    break
                except:
                    print(f"✓ {browser_name} found: {path}")
                    found_browsers.append(browser_name)
                    break

    if not found_browsers:
        print("\n✗ No browsers found!")
        print("\nTo install a browser:")
        print("  Chromium: sudo apt update && sudo apt install -y chromium-browser")
        print("  Firefox:  sudo apt update && sudo apt install -y firefox")
        return False
    else:
        print(f"\n✓ Found {len(found_browsers)} browser(s): {', '.join(found_browsers)}")
        return True


def check_python_packages():
    """Check if required Python packages are installed"""
    print("\n" + "=" * 70)
    print("Checking Python Packages...")
    print("=" * 70)

    required_packages = [
        'selenium',
        'webdriver_manager',
        'streamlit',
        'pandas',
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n✗ Missing {len(missing_packages)} package(s)")
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All required packages are installed")
        return True


def check_driver_support():
    """Check if webdriver-manager can work"""
    print("\n" + "=" * 70)
    print("Testing WebDriver Setup...")
    print("=" * 70)

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager

        print("✓ WebDriver Manager is available")
        print("  Supports: Chrome, Firefox")
        return True
    except ImportError as e:
        print(f"✗ WebDriver Manager not available: {e}")
        return False


def test_scraper_import():
    """Test if the scraper can be imported"""
    print("\n" + "=" * 70)
    print("Testing Scraper Import...")
    print("=" * 70)

    try:
        # Add src directory to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))

        from carousell_scraper import CarousellScraper
        print("✓ Scraper module can be imported")

        # Try to detect browser
        scraper = CarousellScraper()
        browser = scraper._detect_browser()

        if browser:
            print(f"✓ Auto-detected browser: {browser}")
            return True
        else:
            print("✗ Could not auto-detect browser")
            return False

    except Exception as e:
        print(f"✗ Error importing scraper: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all checks"""
    print("\n" + "=" * 70)
    print(" CAROUSELL SCRAPER - SYSTEM CHECK ")
    print("=" * 70)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Browsers", check_browsers),
        ("Python Packages", check_python_packages),
        ("WebDriver Support", check_driver_support),
        ("Scraper Module", test_scraper_import),
    ]

    results = {}

    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n✗ Error running {check_name} check: {e}")
            results[check_name] = False

    # Summary
    print("\n" + "=" * 70)
    print(" SUMMARY ")
    print("=" * 70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {check_name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n" + "=" * 70)
        print("✓ ALL CHECKS PASSED!")
        print("=" * 70)
        print("\nYou're ready to use the scraper!")
        print("\nNext steps:")
        print("  1. Run the Streamlit app:    streamlit run app.py")
        print("  2. Try the examples:          python examples/example_usage.py")
        print("  3. Read the docs:             cat QUICKSTART.md")
        return 0
    else:
        print("\n" + "=" * 70)
        print("✗ SOME CHECKS FAILED")
        print("=" * 70)
        print("\nPlease fix the issues above before using the scraper.")
        print("\nFor help, see: INSTALLATION.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
