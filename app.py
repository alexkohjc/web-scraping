"""
Carousell.sg Web Scraper - Streamlit Frontend
A user-friendly interface for scraping Carousell.sg listings
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from carousell_scraper import scrape_carousell


# Page configuration
st.set_page_config(
    page_title="Carousell.sg Scraper",
    page_icon="🛒",
    layout="wide"
)

# Title and description
st.title("🛒 Carousell.sg Web Scraper")
st.markdown("""
This tool allows you to search and scrape product listings from Carousell.sg.
Simply enter your search term and the maximum number of results you want to retrieve.
""")

# Add a warning
st.warning("⚠️ Please use this tool responsibly and respect Carousell's terms of service. The scraper includes delays to avoid overwhelming the server.")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")

    headless_mode = st.checkbox(
        "Headless Mode",
        value=True,
        help="Run browser in headless mode (no visible window)"
    )

    st.markdown("---")
    st.markdown("""
    ### About
    This scraper uses Selenium to extract product information including:
    - **Item Name**
    - **Price**
    - **Product URL**

    ### Safety Features
    - Random delays between requests (2-5 seconds)
    - Human-like scrolling behavior
    - Proper browser headers
    - Rate limiting
    """)

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        "🔍 Search Term",
        placeholder="e.g., laptop, iPhone, furniture",
        help="Enter what you want to search for on Carousell.sg"
    )

with col2:
    max_results = st.number_input(
        "Max Results",
        min_value=1,
        max_value=100,
        value=20,
        step=5,
        help="Maximum number of results to retrieve"
    )

# Search button
if st.button("🚀 Start Scraping", type="primary", use_container_width=True):
    if not search_query:
        st.error("❌ Please enter a search term!")
    else:
        # Create a placeholder for status updates
        status_placeholder = st.empty()
        progress_bar = st.progress(0)

        with status_placeholder.container():
            st.info(f"🔄 Scraping Carousell.sg for '{search_query}'...")
            st.caption("This may take a while depending on the number of results. Please be patient.")

        try:
            # Perform the scraping using context manager to get scraper instance
            from carousell_scraper import CarousellScraper
            scraper = CarousellScraper(headless=headless_mode)

            try:
                results = scraper.search(query=search_query, max_results=max_results)
            finally:
                # Store screenshot before closing
                debug_screenshot = scraper.debug_screenshot
                scraper.close()

            progress_bar.progress(100)
            status_placeholder.empty()

            # Display results
            if results:
                st.success(f"✅ Successfully scraped {len(results)} items!")

                # Convert to DataFrame
                df = pd.DataFrame(results)

                # Reorder columns for better display
                if 'name' in df.columns and 'price' in df.columns and 'url' in df.columns:
                    df = df[['name', 'price', 'url']]

                # Display statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Items", len(results))
                with col2:
                    # Count items with valid prices
                    valid_prices = df[df['price'] != 'N/A']['price'].count() if 'price' in df.columns else 0
                    st.metric("Items with Price", valid_prices)
                with col3:
                    # Count items with valid URLs
                    valid_urls = df[df['url'] != 'N/A']['url'].count() if 'url' in df.columns else 0
                    st.metric("Valid Links", valid_urls)

                st.markdown("---")

                # Display table with clickable links
                st.subheader("📊 Results")

                # Make URLs clickable in the dataframe
                if 'url' in df.columns:
                    df['url'] = df['url'].apply(
                        lambda x: f'<a href="{x}" target="_blank">View Listing</a>' if x != 'N/A' else 'N/A'
                    )

                # Display as HTML to support clickable links
                st.markdown(
                    df.to_html(escape=False, index=False),
                    unsafe_allow_html=True
                )

                # Download button
                st.markdown("---")
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"carousell_{search_query.replace(' ', '_')}.csv",
                    mime="text/csv"
                )

            else:
                st.warning("⚠️ No results found. The page structure may have changed or no items matched your search.")
                st.info("💡 Try a different search term or check if the website is accessible.")

                # Display debug screenshot if available
                if debug_screenshot:
                    st.subheader("🔍 Debug Screenshot")
                    st.caption("This is what the browser saw when trying to scrape:")
                    st.image(debug_screenshot, caption="Page Screenshot", use_container_width=True)

        except Exception as e:
            progress_bar.empty()
            status_placeholder.empty()
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Please try again or check your internet connection.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Built with Streamlit • Use responsibly and ethically</small>
</div>
""", unsafe_allow_html=True)
