from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    # Freebie.dev returns the Dev instance for this Freebie.
    dev = relationship("Dev", backref="freebies")
    # Freebie.company returns the Company instance for this Freebie.
    company = relationship("Company", backref="freebies")

    def __repr__(self):
        return f'<Freebie {self.item_name} (${self.value})>'
    
    def print_details(self):
        #checks if dev and company exist
        dev_name = self.dev.name if self.dev else "unknown Dev"
        company_name = self.company.name if self.company else "Unknown Company"
        return f"{dev_name} owns a {self.name} from {company_name}."

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer()) 


    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self,dev, item_name, value):
        new_freebie = Freebie(name=item_name, value=value, dev= dev, company = self)
        return new_freebie
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year.asc()).first()

    
        

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

     
    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        # Iterate through each freebie associated with this dev
        for freebie in self.freebies:
            # If the current freebie's name matches the item_name, return True
            if freebie.name == item_name:
                return True
        # If the loop finishes without finding a match, return False
        return False
    

    def give_away(self, target_dev, freebie_to_give):
        # Check if the freebie_to_give actually belongs to the current dev
        if freebie_to_give in self.freebies:
            
            freebie_to_give.dev = target_dev
            
            print(f"{self.name} successfully gave away '{freebie_to_give.name}' to {target_dev.name}.")
            return True
        else:
            print(f"{self.name} cannot give away '{freebie_to_give.name}' because it does not belong to them.")
            return False