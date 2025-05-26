#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your models
from models import Company, Dev, Freebie, Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')

    # Create all tables defined in Base if they don't exist
    Base.metadata.create_all(engine)

    # Create a session factory
    Session = sessionmaker(bind=engine)
    # Create a session instance
    session = Session()

    print("--- Starting Debug Session ---")

    # --- 1. Clear existing data and add your specific seed data ---
    # This ensures your tests always start from your exact known state
    print("Clearing existing data and adding specific seed data...")
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()
    session.commit()

    # Create companies
    google = Company(name="Google", founding_year=1998)
    amazon = Company(name="Amazon", founding_year=1994)
    # Adding another company for oldest_company test, if you want more variety
    microsoft = Company(name="Microsoft", founding_year=1975) 

    # Create devs
    happiness = Dev(name="Happiness")
    samuel = Dev(name="Samuel")
    # Adding another dev for give_away test
    emma = Dev(name="Emma") 

    # Add them to session and commit so they get IDs
    session.add_all([google, amazon, microsoft, happiness, samuel, emma])
    session.commit()

    # Create freebies
    f1_tshirt = Freebie(item_name="T-shirt", value=10, dev=happiness, company=google)
    f2_sticker = Freebie(item_name="Sticker Pack", value=5, dev=samuel, company=amazon)
    f3_diary = Freebie(item_name="Diary", value=15, dev=happiness, company=amazon)
    f4_mousepad = Freebie(item_name="Mousepad", value=20, dev=samuel, company=microsoft) # New freebie

    # Add freebies to the session
    session.add_all([f1_tshirt, f2_sticker, f3_diary, f4_mousepad])
    session.commit()

    print("Specific seed data inserted.")
    print("-" * 30)

    # --- 2. Retrieve Instances (Important for fresh session tests) ---
    # Even if you just created them, it's good practice to retrieve them
    # from the session, especially after a commit.
    happiness = session.query(Dev).filter_by(name="Happiness").first()
    samuel = session.query(Dev).filter_by(name="Samuel").first()
    emma = session.query(Dev).filter_by(name="Emma").first() # Retrieve the new dev

    google = session.query(Company).filter_by(name="Google").first()
    amazon = session.query(Company).filter_by(name="Amazon").first()
    microsoft = session.query(Company).filter_by(name="Microsoft").first() # Retrieve the new company

    f1_tshirt = session.query(Freebie).filter_by(item_name="T-shirt").first()
    f2_sticker = session.query(Freebie).filter_by(item_name="Sticker Pack").first()
    f3_diary = session.query(Freebie).filter_by(item_name="Diary").first()
    f4_mousepad = session.query(Freebie).filter_by(item_name="Mousepad").first()


    # --- 3. Test Relationship Attributes ---
    print("\n--- Testing Relationship Attributes ---")
    if f1_tshirt:
        print(f"Freebie: {f1_tshirt.item_name}")
        print(f"  -> Dev: {f1_tshirt.dev.name}")
        print(f"  -> Company: {f1_tshirt.company.name}")

    if happiness:
        print(f"\nDev: {happiness.name}")
        print(f"  -> Freebies: {[f.item_name for f in happiness.freebies]}")
        # Using set to get unique companies
        print(f"  -> Companies: {[c.name for c in set(happiness.companies)]}")

    if google:
        print(f"\nCompany: {google.name}")
        print(f"  -> Freebies: {[f.item_name for f in google.freebies]}")
        # Using set to get unique devs
        print(f"  -> Devs: {[d.name for d in set(google.devs)]}")
    print("-" * 30)

    # --- 4. Test Aggregate Methods ---

    # Freebie.print_details()
    print("\n--- Testing Freebie.print_details() ---")
    if f1_tshirt:
        print(f"Details for T-Shirt: {f1_tshirt.print_details()}") # Expected: Happiness owns a T-shirt from Google.
    print("-" * 30)

    # Company.give_freebie(dev, item_name, value)
    print("\n--- Testing Company.give_freebie() ---")
    if google and samuel:
        print(f"Samuel's freebies BEFORE new: {[f.item_name for f in samuel.freebies]}")
        new_freebie_cap = google.give_freebie(samuel, "Google Cap", 25)
        session.add(new_freebie_cap)
        session.commit() 
        session.refresh(samuel) # Refresh samuel to see the newly added freebie
        print(f"Samuel's freebies AFTER new: {[f.item_name for f in samuel.freebies]}")
        print(f"New freebie details: {new_freebie_cap.print_details()}")
    print("-" * 30)

    # Company.oldest_company()
    print("\n--- Testing Company.oldest_company() ---")
    oldest = Company.oldest_company(session)
    if oldest:
        print(f"The oldest company is: {oldest.name} (founded in {oldest.founding_year})") # Expected: Microsoft
    print("-" * 30)

    # Dev.received_one(item_name)
    print("\n--- Testing Dev.received_one() ---")
    if happiness:
        print(f"Did Happiness receive a 'T-shirt'? {happiness.received_one('T-shirt')}")     # Expected: True
        print(f"Did Happiness receive a 'Laptop'? {happiness.received_one('Laptop')}") # Expected: False
    print("-" * 30)

    # Dev.give_away(dev, freebie)
    print("\n--- Testing Dev.give_away() ---")
    if happiness and emma and f1_tshirt and f2_sticker:
        print(f"Happiness's freebies BEFORE give_away: {[f.item_name for f in happiness.freebies]}")
        print(f"Emma's freebies BEFORE give_away: {[f.item_name for f in emma.freebies]}")

        # Scenario 1: Happiness gives away their T-shirt to Emma
        print("\nAttempting to give away T-shirt (Happiness owns it):")
        happiness.give_away(emma, f1_tshirt)
        session.commit() # Commit the change in ownership
        session.refresh(happiness) # Refresh both devs to see the change
        session.refresh(emma)
        session.refresh(f1_tshirt) # Refresh freebie to reflect new owner
        print(f"Happiness's freebies AFTER give_away: {[f.item_name for f in happiness.freebies]}")
        print(f"Emma's freebies AFTER give_away: {[f.item_name for f in emma.freebies]}")
        print(f"T-Shirt's current owner: {f1_tshirt.dev.name}")


        # Scenario 2: Happiness tries to give away Samuel's Sticker Pack (which they don't own) to Emma
        print("\nAttempting to give away Sticker Pack (Happiness DOES NOT own it):")
        happiness.give_away(emma, f2_sticker) # This should print the "cannot give away" message
        session.commit() # No change should be committed
        session.refresh(happiness)
        session.refresh(emma)
        print(f"Happiness's freebies (should be unchanged): {[f.item_name for f in happiness.freebies]}")
        print(f"Emma's freebies (should be unchanged): {[f.item_name for f in emma.freebies]}")

    print("-" * 30)
    print("\n--- Debug Session Complete ---")

    
    import ipdb; ipdb.set_trace()