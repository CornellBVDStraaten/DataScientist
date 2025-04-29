import os
os.environ['NLTK_DATA'] = os.path.expanduser('~/AppData/Roaming/nltk_data')  # Force lookup path
import nltk
nltk.data.path.append(os.path.expanduser('~/AppData/Roaming/nltk_data'))

import pandas as pd
import string 
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from tqdm import tqdm

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

stop_words = set(stopwords.words('english'))
stop_words.discard('not')

lemmatizer = WordNetLemmatizer()

tqdm.pandas()

df = pd.read_csv("./Hotel_Reviews_Cleaned.csv")
dfTest = df.copy()

def clean_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = ' '.join(text.split())  # Remove extra whitespace
    return text

def remove_stopwords(text):
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    text = ' '.join(words)
    return text

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to noun
    
def lemmatize(text):
    words = text.split()
    tagged_words = pos_tag(words)
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in tagged_words]
    text = ' '.join(lemmatized_words)
    return text

# Reduce memory usage / remove need for check in functions
dfTest['Positive_Review'] = dfTest['Positive_Review'].astype(str)
dfTest['Negative_Review'] = dfTest['Negative_Review'].astype(str)
for col in ['Positive_Review', 'Negative_Review']:
    if col in dfTest.columns:
        tqdm.pandas(desc=f"Processing {col}")
        dfTest[col] = dfTest[col].progress_apply(clean_text)
        dfTest[col] = dfTest[col].progress_apply(lemmatize)
        dfTest[col] = dfTest[col].progress_apply(remove_stopwords)

positive = dfTest[['Positive_Review']].copy()
positive['text'] = positive['Positive_Review']
positive['label'] = 1
positive = positive[~positive['text'].str.strip().str.lower().eq('positive')]

negative = dfTest[['Negative_Review']].copy()
negative['text'] = negative['Negative_Review']
negative['label'] = 0
negative = negative[~negative['text'].str.strip().str.lower().eq('negative')]

final_df = pd.concat([positive[['text', 'label']], negative[['text', 'label']]]).dropna().reset_index(drop=True)

final_df.to_csv("./Hotel_Reviews_Prepared.csv", index=False)
# End goal: One CSV with 2 columns, text and a boolean if it is negative or positive