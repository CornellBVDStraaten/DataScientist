import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Hotel Reviews Analysis")

df = pd.read_csv("./Hotel_Reviews_Original.csv")
df.columns = df.columns.str.strip().str.lower()

df['full_review'] = df['positive_review'].astype(str) + " " + df['negative_review'].astype(str)

st.subheader("Data Preview")
st.dataframe(df.head())

st.subheader("Hotels with the Most Reviews")
review_counts = df['hotel_name'].value_counts().head(10)
fig2, ax2 = plt.subplots(figsize=(10, 5))
review_counts.plot(kind='bar', ax=ax2, color='orange')
ax2.set_ylabel("Review Count")
ax2.set_title("Most Reviewed Hotels")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig2)

st.subheader("Positive vs Negative Review Lengths")
df['pos_length'] = df['positive_review'].astype(str).apply(len)
df['neg_length'] = df['negative_review'].astype(str).apply(len)
fig5, ax5 = plt.subplots()
ax5.hist([df['pos_length'], df['neg_length']], bins=30, label=['Positive', 'Negative'],
         color=['blue', 'red'], alpha=0.6)
ax5.set_xlabel("Length (characters)")
ax5.set_ylabel("Count")
ax5.set_title("Length of Positive vs Negative Reviews")
ax5.legend()
st.pyplot(fig5)

hotel_avg = df.groupby('hotel_name')['average_score'].mean().reset_index()
hotel_avg = hotel_avg.sort_values(by='average_score', ascending=False)

st.subheader("Average Score per Hotel")
st.dataframe(hotel_avg)
