#!/usr/bin/env python3

# Script goes here!

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

# Connect to your database
engine = create_engine('sqlite:///freebies.db') 
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist 
Base.metadata.create_all(engine)

# Clear old data 
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()
session.commit()

# Create companies
google = Company(name="Google", founding_year=1998)
amazon = Company(name="Amazon", founding_year=1994)

# Create devs
happiness = Dev(name="Happiness")
samuel = Dev(name="Samuel")

# Add them to session and commit so they get IDs
session.add_all([google, amazon, happiness, samuel ])
session.commit()

# Create freebies
f1 = Freebie(item_name="T-shirt", value=10, dev_id=happiness.id, company_id=google.id)
f2 = Freebie(item_name="Sticker Pack", value=5, dev_id=samuel.id, company_id=amazon.id)
f3 = Freebie(item_name="Diary", value=15, dev_id=happiness.id, company_id=amazon.id)

# Add freebies to the session
session.add_all([f1, f2, f3])
session.commit()

print("Seeding complete! Sample data inserted.")

