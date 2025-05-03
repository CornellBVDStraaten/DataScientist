from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

engine = create_engine('mysql+pymysql://root:usxrryoa@localhost/hotel')
Base = declarative_base()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_text = Column(String(3000))
    is_positive_review = Column(Boolean)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Inserting data from prepared csv
Session = sessionmaker(bind=engine)
session = Session()

# Uncomment to re-add data
# csv_file_path = 'Hotel_Reviews_Prepared.csv'
# reviews_df = pd.read_csv(csv_file_path)

# reviews_df.dropna(subset=['text', 'label'], inplace=True)
# for index, row in reviews_df.iterrows():
#     review = Review(
#         review_text=row['text'],
#         is_positive_review=row['label']
#     )
#     session.add(review)

# session.commit()

# Creating stored procedure
sp_query = """
CREATE PROCEDURE GetReviews()
BEGIN
    SELECT review_text, is_positive_review FROM reviews;
END;
"""

conn = engine.raw_connection()
cursor = conn.cursor()
cursor.execute(sp_query)
conn.commit()
cursor.close()
conn.close()

session.close()

