import pandas as pd
from sqlalchemy import create_engine


#engine = create_engine('mysql+mysqlconnector://root:admin@localhost/hotelcleaned')
# OR
engine = create_engine('mysql+pymysql://root:admin@localhost/hotel')
# OR MS SQLsever
#engine = create_engine('mssql+pymssql://username fvpdbadmin:password EsEpIdGbBj@35@fvpdb.database.windows.net/Frank')
# FIRST EMBEDDED RAW SQL

dfhotel = pd.read_sql("SELECT * FROM hotel_reviews_labeled", con=engine)
dfhotel.head(10)

df_precleaned=dfhotel[['review']]
y=dfhotel['label']



### Cleaning simple or more advanced
import re

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
NO_SPACE = ""
SPACE = " "

def preprocess_reviews(reviews):
    
    reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]
    
    return reviews

dfhotel["review_cleaned"]=preprocess_reviews(df_precleaned["review"])


# create db first in MySQL
engine = create_engine('mysql+mysqlconnector://root:admin@localhost/hotel')

dfhotel.to_sql(name='hotel_reviews_cleaned',con=engine,if_exists='fail',index=False, chunksize=1000) 



# skip advanced cleaning 
###  stopwords / own stopwords  stemming / lemmatizing
# splitting the data, no crossfold validation

X= dfhotel['review_cleaned']
y= dfhotel['label']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test= train_test_split(X ,y, train_size=0.8 ,random_state=0)

# start most important step: Counting the words
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(binary=False)

X_train_cv=cv.fit_transform(X_train)
X_test_cv=cv.transform(X_test)

### pick 3 models

