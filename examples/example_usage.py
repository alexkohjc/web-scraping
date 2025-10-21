"""
Example usage of the Carousell.sg scraper

This script demonstrates different ways to use the scraper programmatically.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the scraper
sys.path.append(str(Path(__file__).parent.parent))

from src.carousell_scraper import scrape_carousell, CarousellScraper
import pandas as pd


def example_1_simple_search():
    """Example 1: Simple search using the convenience function"""
    print("=" * 70)
    print("Example 1: Simple Search for Laptops")
    print("=" * 70)

    results = scrape_carousell(
        query="laptop",
        max_results=10,
        headless=True
    )

    print(f"\nFound {len(results)} results\n")

    for i, item in enumerate(results, 1):
        print(f"Item {i}:")
        print(f"  Name: {item['name']}")
        print(f"  Price: {item['price']}")
        print(f"  URL: {item['url']}")
        print()


def example_2_with_context_manager():
    """Example 2: Using the scraper with context manager"""
    print("=" * 70)
    print("Example 2: Using Context Manager")
    print("=" * 70)

    with CarousellScraper(headless=True, delay_range=(3, 5)) as scraper:
        results = scraper.search("iPhone", max_results=15)

        print(f"\nFound {len(results)} results\n")

        for item in results[:5]:  # Show first 5 results
            print(f"Name: {item['name']}")
            print(f"Price: {item['price']}")
            print(f"URL: {item['url'][:50]}...")  # Truncate long URLs
            print("-" * 50)


def example_3_save_to_csv():
    """Example 3: Search and save results to CSV"""
    print("=" * 70)
    print("Example 3: Save Results to CSV")
    print("=" * 70)

    search_term = "furniture"
    print(f"\nSearching for: {search_term}")

    results = scrape_carousell(
        query=search_term,
        max_results=20,
        headless=True
    )

    if results:
        # Convert to DataFrame
        df = pd.DataFrame(results)

        # Save to CSV
        output_file = f"carousell_{search_term}_results.csv"
        df.to_csv(output_file, index=False)

        print(f"\n✓ Saved {len(results)} results to {output_file}")
        print("\nFirst 5 rows of the DataFrame:")
        print(df.head())
    else:
        print("No results found")


def example_4_multiple_searches():
    """Example 4: Perform multiple searches"""
    print("=" * 70)
    print("Example 4: Multiple Searches")
    print("=" * 70)

    search_terms = ["laptop", "phone", "camera"]
    all_results = {}

    with CarousellScraper(headless=True) as scraper:
        for term in search_terms:
            print(f"\nSearching for: {term}")
            results = scraper.search(term, max_results=5)
            all_results[term] = results
            print(f"  Found {len(results)} results")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    for term, results in all_results.items():
        print(f"\n{term.upper()}:")
        if results:
            for i, item in enumerate(results[:3], 1):  # Show top 3
                print(f"  {i}. {item['name'][:40]} - {item['price']}")
        else:
            print("  No results")


def example_5_filter_results():
    """Example 5: Search and filter results"""
    print("=" * 70)
    print("Example 5: Search and Filter Results")
    print("=" * 70)

    results = scrape_carousell(
        query="laptop",
        max_results=30,
        headless=True
    )

    print(f"\nTotal results: {len(results)}")

    # Filter for items with valid prices
    items_with_price = [item for item in results if item['price'] != 'N/A' and '$' in item['price']]
    print(f"Items with prices: {len(items_with_price)}")

    # Filter for items with valid URLs
    items_with_url = [item for item in results if item['url'] != 'N/A']
    print(f"Items with URLs: {len(items_with_url)}")

    # Try to extract numeric price for sorting (basic example)
    def extract_price(price_str):
        """Extract numeric value from price string"""
        try:
            import re
            match = re.search(r'[\d,]+(?:\.\d{2})?', price_str)
            if match:
                return float(match.group().replace(',', ''))
        except:
            pass
        return float('inf')

    # Sort by price
    items_sorted = sorted(items_with_price, key=lambda x: extract_price(x['price']))

    print("\n" + "-" * 70)
    print("Top 5 cheapest items:")
    print("-" * 70)

    for i, item in enumerate(items_sorted[:5], 1):
        print(f"{i}. {item['name'][:45]}")
        print(f"   Price: {item['price']}")
        print()


def main():
    """Run all examples"""
    print("\n")
    print("=" * 70)
    print(" CAROUSELL.SG SCRAPER - EXAMPLE USAGE ")
    print("=" * 70)
    print()

    examples = [
        ("Simple Search", example_1_simple_search),
        ("Context Manager", example_2_with_context_manager),
        ("Save to CSV", example_3_save_to_csv),
        ("Multiple Searches", example_4_multiple_searches),
        ("Filter Results", example_5_filter_results),
    ]

    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\nWhich example would you like to run?")
    print("Enter a number (1-5), 'all' to run all, or 'q' to quit: ", end="")

    choice = input().strip().lower()

    if choice == 'q':
        print("Goodbye!")
        return

    if choice == 'all':
        for name, func in examples:
            print("\n\n")
            try:
                func()
            except Exception as e:
                print(f"Error in {name}: {str(e)}")
            print("\n" + "=" * 70)
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        idx = int(choice) - 1
        try:
            examples[idx][1]()
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
