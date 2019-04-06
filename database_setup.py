import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class Customer(Base):
    '''
    Schema of customers
    '''
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    dob = Column(Date, nullable=False)
    updated_at = Column(DateTime,
        nullable=False,
        default=datetime.datetime.now())

    # Serialization function for JSON API requests
    @property
    def serialize(self):
        return {
            'name': self.name,
            'dob': self.dob,
        }

engine = create_engine('postgresql+psycopg2://giga:agig@localhost/giga')
Base.metadata.create_all(engine)
