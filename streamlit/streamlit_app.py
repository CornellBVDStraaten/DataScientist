import streamlit as st

# Define the pages
main_page = st.Page("00_data_metadata.py", title="Metadata Info")
page_2 = st.Page("01_data_insights.py", title="Data Insights")
page_3 = st.Page("02_naive_bayes.py", title="Model 1: Naive Bayes")
page_4 = st.Page("03_logistic_regression.py", title="Model 2: Logistic Regression")
page_5 = st.Page("04_svm.py", title="Model 3: SVM")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3, page_4, page_5])

# Run the selected page
pg.run()