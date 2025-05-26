#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import Company, Dev, Freebie, Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    Session = Session()
    import ipdb; ipdb.set_trace()
