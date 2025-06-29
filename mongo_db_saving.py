import pandas as pd
from pymongo import MongoClient

files = [
    ('Hotel_Reviews_Cleaned.csv', 'reviews_cleaned'),
    ('Hotel_Reviews_Prepared.csv', 'reviews_prepared')
]

# default mongo port
client = MongoClient('mongodb://localhost:27017/')
db = client['hotel_reviews_db'] 

for file_path, collection_name in files:
    print(f"\nProcessing: {file_path}")

    df = pd.read_csv(file_path)

    # df to dict for Mongo (JSON kindof)
    data_dict = df.to_dict(orient='records')

    collection = db[collection_name]
    result = collection.insert_many(data_dict)

    print(f"Doc Count: {len(result.inserted_ids)} into '{collection_name}'.")
    print(collection.find_one())