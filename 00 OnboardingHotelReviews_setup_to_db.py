import pandas as pd

dfhotel =pd.read_csv("Hotel_Reviews.csv")

# dfhotel.head(5)
# dfhotel.dtypes

# dfhotel.isnull().sum()

# import plotly.express as px
# fig = px.histogram(dfhotel, x="Review_Total_Negative_Word_Counts")
# fig.show()

# old skool
dfhotelfiltered=dfhotel[dfhotel['Review_Total_Negative_Word_Counts']>=5]


#  OR new kid 
dfhotelfiltered1=(
                    dfhotel
                    .loc[lambda df: df['Review_Total_Negative_Word_Counts'] >= 5]
                )


dfhotelfiltered=dfhotel[(dfhotel['Review_Total_Negative_Word_Counts']>=5) & (dfhotel['Review_Total_Positive_Word_Counts']>=5)]

dfhotelFilteredNeg=(
    dfhotelfiltered
    .loc[:,['Negative_Review']]
)

dfhotelFilteredNeg['label']=0


dfhotelFilteredPos=(
    dfhotelfiltered
    .loc[:,['Positive_Review']]
)

dfhotelFilteredPos['label']=1

dfhotelFilteredNeg= dfhotelFilteredNeg.rename({'Negative_Review': 'review'}, axis=1)  
dfhotelFilteredPos= dfhotelFilteredPos.rename({'Positive_Review': 'review'}, axis=1)

dfhotelCombi=pd.concat([dfhotelFilteredNeg, dfhotelFilteredPos], axis=0)
dfhotelCombi.head(20)

dfhotelCombishuffle = dfhotelCombi.sample(frac=1).reset_index(drop=True)
dfhotelCombishuffle.head(20)

# # to MySQL on local machine

from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:admin@localhost/hotel')

dfhotelCombishuffle.to_sql(name='hotel_reviews_labeled',con=engine,if_exists='fail',index=False, chunksize=1000) 

# # to MySQL on OEGE

engine = create_engine('mysql+mysqlconnector://odepj:5fuemohADye3QZe/@oege.ie.hva.nl/zodepj')

dfhotelCombishuffle.to_sql(name='hotelreviewslabeled',con=engine,if_exists='fail',index=False, chunksize=1000) 


# # to MongoDb
# from pymongo import MongoClient
# import pandas as pd

# # Connect to mongodb
# client = MongoClient("localhost:27017")
# db = client.hotel

# # Load csv and put it in MonogDB

# db.hotel_reviews_cleaned.insert_many(dfhotelCombishuffle.to_dict('records'))
