import streamlit as sl
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import re

sl.title('Data Insights')

engine = create_engine('mysql+pymysql://root:usxrryoa@localhost/hotel')
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.raw_connection()
cursor = conn.cursor()

@sl.cache_data
def load_data_db():
    cursor.execute("CALL GetReviews()")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=['review_text', 'is_positive_review'])

@sl.cache_data
def basic_clean(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text

@sl.cache_data
def generate_wordcloud_from_df(df, colname):
    text = ' '.join(df[colname].dropna().astype(str).tolist())
    text = basic_clean(text)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud.to_array()

df = load_data_db()

sl.text('Wordcloud of processed reviews')
wordcloud_array = generate_wordcloud_from_df(df, 'review_text')
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud_array, interpolation='bilinear')
ax.axis('off')
sl.pyplot(fig)


@sl.cache_data
def load_data_original():
    return pd.read_csv("./Hotel_Reviews_Original.csv")

@sl.cache_data
def generate_wordcloud_from_original(df):
    combined = df['Negative_Review'].fillna('') + ' ' + df['Positive_Review'].fillna('')
    text = basic_clean(' '.join(combined))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud.to_array()

dfNonProcessed = load_data_original()

sl.text('Wordcloud of non-processed reviews')
wordcloud_array_orig = generate_wordcloud_from_original(dfNonProcessed)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud_array_orig, interpolation='bilinear')
ax.axis('off')
sl.pyplot(fig)
