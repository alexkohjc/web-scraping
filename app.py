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

# Add warnings
st.warning("⚠️ Please use this tool responsibly and respect Carousell's terms of service. The scraper includes delays to avoid overwhelming the server.")
st.info("💡 **Tip:** Keep 'Headless Mode' disabled in the sidebar for best results. Headless mode often triggers CAPTCHA verification.")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")

    dev_mode = st.checkbox(
        "🔧 Dev Mode",
        # value=False,
        value=True,
        help="Enable developer mode with pre-filled search term"
    )

    headless_mode = st.checkbox(
        "Headless Mode",
        value=False,
        help="Run browser in headless mode (no visible window). Note: Headless mode may trigger CAPTCHA - keep this unchecked for better results."
    )

    st.markdown("---")
    st.markdown("""
    ### About
    This scraper uses Selenium to extract product information including:
    - **Item Name**
    - **Price**
    - **Condition** (brand new, lightly used, etc.)
    - **Seller Name**
    - **Posting Time**
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
        value="rolex daytona" if dev_mode else "",
        placeholder="e.g., laptop, iPhone, furniture",
        help="Enter what you want to search for on Carousell.sg"
    )

with col2:
    max_results = st.number_input(
        "Max Results",
        min_value=1,
        max_value=100,
        value=5,
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
                column_order = []
                if 'item_name' in df.columns:
                    column_order.append('item_name')
                if 'price' in df.columns:
                    column_order.append('price')
                if 'condition' in df.columns:
                    column_order.append('condition')
                if 'seller' in df.columns:
                    column_order.append('seller')
                if 'time' in df.columns:
                    column_order.append('time')
                if 'url' in df.columns:
                    column_order.append('url')

                if column_order:
                    df = df[column_order]

                # Display statistics (before capitalizing headers)
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

                # Make URLs clickable in the dataframe (before capitalizing)
                if 'url' in df.columns:
                    df['url'] = df['url'].apply(
                        lambda x: f'<a href="{x}" target="_blank">View Listing</a>' if x != 'N/A' else 'N/A'
                    )

                # Capitalize column headers (do this last)
                df.columns = df.columns.str.capitalize()

                st.markdown("---")

                # Display table with clickable links
                st.subheader("📊 Results")

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
