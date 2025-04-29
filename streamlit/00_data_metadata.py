import streamlit as sl;
import pandas as pd;

df = pd.read_csv("./Hotel_Reviews_Original.csv")

sl.table(df.head())