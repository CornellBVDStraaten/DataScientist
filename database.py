from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

engine = create_engine('mysql+pymysql://root:usxrryoa@localhost/hotel')
Base = declarative_base()

# Define the Review table
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_text = Column(String(3000))
    is_positive_review = Column(Boolean)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Load the data
csv_file_path = 'Hotel_Reviews_Prepared.csv'  # Make sure the CSV path is correct
reviews_df = pd.read_csv(csv_file_path)

reviews_df.dropna(subset=['text', 'label'], inplace=True)

# Start a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data
for index, row in reviews_df.iterrows():
    review = Review(
        review_text=row['text'],
        is_positive_review=row['label']
    )
    session.add(review)

# Commit the transaction
session.commit()

# Close the session
session.close()