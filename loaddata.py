import csv

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Customer


engine = create_engine('postgresql+psycopg2://giga:agig@localhost/giga')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# sample data
mockdata = [0] * 50
with open('sample_data.csv', 'r') as f:
    rawdata = csv.reader(f)
    for i, row in enumerate(rawdata):
        mockdata[i] = {'name':row[0], 'dob':datetime.strptime(row[1], r'%d/%m/%Y')}

def load_data(data):
    for customer in add_entries(data):
        session.add(customer)


def add_entries(data):
    for row in data:
        customer = Customer(name=row['name'], dob=row['dob'])
        yield customer


if __name__ == '__main__':
    load_data(mockdata)
    session.commit()