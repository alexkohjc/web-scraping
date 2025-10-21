#!/usr/bin/env python3
"""
Diagnostic script to identify browser/driver issues
"""

import os
import subprocess
import shutil
from pathlib import Path


def check_chromedriver_deps():
    """Check if ChromeDriver has all required dependencies"""
    print("=" * 70)
    print("Checking ChromeDriver Dependencies...")
    print("=" * 70)

    # Find chromedriver
    wdm_path = Path.home() / ".wdm" / "drivers" / "chromedriver"

    if not wdm_path.exists():
        print("ChromeDriver not yet downloaded by webdriver-manager")
        return None

    # Find the most recent chromedriver
    chromedriver_paths = list(wdm_path.rglob("chromedriver"))

    if not chromedriver_paths:
        print("No ChromeDriver found in ~/.wdm")
        return None

    chromedriver = chromedriver_paths[0]
    print(f"Found ChromeDriver: {chromedriver}")

    # Check dependencies with ldd
    try:
        result = subprocess.run(
            ["ldd", str(chromedriver)],
            capture_output=True,
            text=True,
            timeout=10
        )

        print("\nChecking shared library dependencies...\n")

        missing = []
        for line in result.stdout.split('\n'):
            if "not found" in line:
                lib = line.split("=>")[0].strip()
                missing.append(lib)
                print(f"✗ MISSING: {lib}")
            elif "=>" in line and line.strip():
                lib = line.split("=>")[0].strip()
                # Only show important ones
                if any(x in lib for x in ['libnss', 'libnspr', 'libgobject', 'libgdk']):
                    print(f"✓ Found: {lib}")

        if missing:
            print(f"\n✗ Missing {len(missing)} required libraries!")
            print("\nTo fix, run:")
            print("  sudo apt update")
            print("  sudo apt install -y libnss3 libnss3-dev libnspr4 libnspr4-dev")
            return False
        else:
            print("\n✓ All ChromeDriver dependencies satisfied!")
            return True

    except Exception as e:
        print(f"Error checking dependencies: {e}")
        return None


def check_firefox():
    """Check if Firefox is properly installed"""
    print("\n" + "=" * 70)
    print("Checking Firefox...")
    print("=" * 70)

    firefox_path = shutil.which("firefox")

    if not firefox_path:
        print("✗ Firefox not found")
        print("\nTo install Firefox:")
        print("  sudo apt update && sudo apt install -y firefox")
        return False

    print(f"✓ Firefox found: {firefox_path}")

    # Try to get version
    try:
        result = subprocess.run(
            ["firefox", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"  Version: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"  Warning: Could not get version: {e}")
        return True


def check_chromium():
    """Check if Chromium is properly installed"""
    print("\n" + "=" * 70)
    print("Checking Chromium...")
    print("=" * 70)

    chromium_commands = ["chromium-browser", "chromium", "google-chrome", "chrome"]
    chromium_path = None

    for cmd in chromium_commands:
        path = shutil.which(cmd)
        if path:
            chromium_path = path
            print(f"✓ Chromium found: {path}")
            break

    if not chromium_path:
        print("✗ Chromium/Chrome not found")
        print("\nTo install Chromium:")
        print("  sudo apt update && sudo apt install -y chromium-browser")
        return False

    # Try to get version
    try:
        result = subprocess.run(
            [chromium_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"  Version: {result.stdout.strip()}")
    except Exception as e:
        print(f"  Warning: Could not get version: {e}")

    return True


def test_selenium_chrome():
    """Try to actually start Chrome with Selenium"""
    print("\n" + "=" * 70)
    print("Testing Selenium with Chrome...")
    print("=" * 70)

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        print("Setting up Chrome driver...")

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("✓ Successfully started Chrome!")
        driver.quit()
        return True

    except Exception as e:
        print(f"✗ Failed to start Chrome: {e}")
        return False


def test_selenium_firefox():
    """Try to actually start Firefox with Selenium"""
    print("\n" + "=" * 70)
    print("Testing Selenium with Firefox...")
    print("=" * 70)

    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager

        print("Setting up Firefox driver...")

        firefox_options = Options()
        firefox_options.add_argument("--headless")

        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)

        print("✓ Successfully started Firefox!")
        driver.quit()
        return True

    except Exception as e:
        print(f"✗ Failed to start Firefox: {e}")
        return False


def main():
    """Run all diagnostics"""
    print("\n" + "=" * 70)
    print(" CAROUSELL SCRAPER - DIAGNOSTICS ")
    print("=" * 70)
    print()

    # Check browsers
    chromium_ok = check_chromium()
    firefox_ok = check_firefox()

    # Check ChromeDriver dependencies
    chromedriver_deps_ok = check_chromedriver_deps()

    # Try actual Selenium tests
    print("\n" + "=" * 70)
    print("SELENIUM TESTS")
    print("=" * 70)

    selenium_chrome_ok = False
    selenium_firefox_ok = False

    if chromium_ok:
        selenium_chrome_ok = test_selenium_chrome()

    if firefox_ok:
        selenium_firefox_ok = test_selenium_firefox()

    # Summary
    print("\n" + "=" * 70)
    print(" SUMMARY & RECOMMENDATIONS ")
    print("=" * 70)

    if selenium_firefox_ok:
        print("\n✓ FIREFOX WORKS - RECOMMENDED")
        print("\nYour scraper should work with Firefox.")
        print("You can start using it now!")

    elif selenium_chrome_ok:
        print("\n✓ CHROME WORKS - RECOMMENDED")
        print("\nYour scraper should work with Chrome.")
        print("You can start using it now!")

    elif chromium_ok and chromedriver_deps_ok is False:
        print("\n⚠ CHROME NEEDS DEPENDENCIES")
        print("\nChrome is installed but ChromeDriver is missing libraries.")
        print("\nFix it with:")
        print("  sudo apt update")
        print("  sudo apt install -y libnss3 libnss3-dev libnspr4 libnspr4-dev")

    elif not firefox_ok and not chromium_ok:
        print("\n✗ NO BROWSER INSTALLED")
        print("\nYou need to install a browser:")
        print("\nOption 1 (Recommended): Install Firefox")
        print("  sudo apt update && sudo apt install -y firefox")
        print("\nOption 2: Install Chromium + dependencies")
        print("  sudo apt update")
        print("  sudo apt install -y chromium-browser libnss3 libnspr4")

    else:
        print("\n⚠ NEEDS ATTENTION")
        print("\nSome issues were detected. Review the output above.")
        print("\nQuickest solution: Install Firefox")
        print("  sudo apt update && sudo apt install -y firefox")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
