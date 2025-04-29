import streamlit as st

# Define the pages
main_page = st.Page("00_data_metadata.py", title="Metadata Info")
page_2 = st.Page("01_data_insights.py", title="Data Insights")

# Set up navigation
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()