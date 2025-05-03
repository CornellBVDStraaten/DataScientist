import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
import joblib
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

st.title("Model: Naive Bayes")

engine = create_engine('mysql+pymysql://root:usxrryoa@localhost/hotel')
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.raw_connection()
cursor = conn.cursor()

@st.cache_data
def load_data():
    cursor.execute("CALL GetReviews()")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows, columns=['review_text', 'is_positive_review'])
    # df = pd.read_csv('Hotel_Reviews_Prepared.csv')
    df.dropna(subset=['review_text'], inplace=True)
    return df

df = load_data()

MODEL_FILENAME = "sentiment_model.pkl"

@st.cache_data
def train_and_save_model(X_train, y_train):
    model = make_pipeline(TfidfVectorizer(
        max_features=10000,
        min_df=2,
        max_df=0.9,
        sublinear_tf=True,
        ngram_range=(1, 2)
    ), BernoulliNB())
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_FILENAME)
    return model

@st.cache_resource
def load_or_train_model(X, y):
    if os.path.exists(MODEL_FILENAME):
        model = joblib.load(MODEL_FILENAME)
        return model
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = train_and_save_model(X_train, y_train)
        return model

X = df['review_text']
y = df['is_positive_review']

model = load_or_train_model(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
st.write(f"Model accuracy on test set: **{accuracy*100:.2f}%**")

st.subheader("Enter your hotel review:")
user_input = st.text_area("Write your review here", "")

if st.button("Predict Sentiment"):
    if user_input.strip() == "":
        st.warning("Please enter a review before predicting.")
    else:
        prediction = model.predict([user_input])[0]
        probability = model.predict_proba([user_input])[0]

        if prediction == 1:
            st.success(f"Positive Review ({probability[1]*100:.2f}% confidence)")
        else:
            st.error(f"Negative Review ({probability[0]*100:.2f}% confidence)")

if st.button('Reset Cache'):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Cleared.")
