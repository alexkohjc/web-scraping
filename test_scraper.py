#!/usr/bin/env python3
"""
Simple test script for Carousell scraper
No Streamlit needed - runs entirely in terminal
"""

from src.carousell_scraper import scrape_carousell
import pandas as pd


def main():
    print("=" * 70)
    print(" CAROUSELL.SG SCRAPER - SIMPLE TEST ")
    print("=" * 70)
    print()

    # Get search term from user
    search_term = input("Enter search term (or press Enter for 'laptop'): ").strip()
    if not search_term:
        search_term = "laptop"

    # Get max results
    max_str = input("Max results (or press Enter for '10'): ").strip()
    max_results = int(max_str) if max_str.isdigit() else 10

    print()
    print(f"Searching for '{search_term}' (max {max_results} results)...")
    print("This may take 30-60 seconds. Please wait...")
    print()

    try:
        # Run the scraper
        results = scrape_carousell(
            query=search_term,
            max_results=max_results,
            headless=True  # No GUI needed - perfect for WSL2!
        )

        print()
        print("=" * 70)
        print(" RESULTS ")
        print("=" * 70)
        print()

        if results:
            # Convert to DataFrame for nice formatting
            df = pd.DataFrame(results)

            print(f"Found {len(results)} items:\n")

            # Print each result
            for i, row in df.iterrows():
                print(f"{i+1}. {row['name']}")
                print(f"   Price: {row['price']}")
                print(f"   URL: {row['url']}")
                print()

            # Save to CSV
            csv_filename = f"carousell_{search_term.replace(' ', '_')}_results.csv"
            df.to_csv(csv_filename, index=False)
            print("=" * 70)
            print(f"✓ Results saved to: {csv_filename}")
            print("=" * 70)

        else:
            print("No results found. Try a different search term.")

    except Exception as e:
        print()
        print("=" * 70)
        print(" ERROR ")
        print("=" * 70)
        print(f"\n{e}\n")

        if "No supported browser found" in str(e):
            print("You need to install Firefox or Chrome:")
            print("  sudo apt update && sudo apt install -y firefox")
        elif "Failed to setup Chrome" in str(e):
            print("Chrome is missing dependencies. Try Firefox instead:")
            print("  sudo apt update && sudo apt install -y firefox")

        print()


if __name__ == "__main__":
    main()
