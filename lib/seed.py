#!/usr/bin/env python3

# Script goes here!
from your_module_name import Base, engine  # engine should be your SQLAlchemy engine
Base.metadata.create_all(engine)