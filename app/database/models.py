from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy import Column, Integer, String, DECIMAL

Base = declarative_base()


class RouteORM(Base):
    __tablename__ = "journeys_asloboda"
    id = Column(Integer, primary_key=True)
    origin = Column(String(255))
    destination = Column(String(255))
    departure = Column(TIMESTAMP)
    arrival = Column(TIMESTAMP)
    carrier = Column(String(255))
    vehicle_type = Column(String(255))
    price = Column(DECIMAL(10,2))
    currency = Column(String(3))
    source_id = Column(String(255))
    destination_id = Column(String(255))
    free_seats = Column(Integer)


class RoutePublicORM(Base):
    __tablename__ = "journeys"
    id = Column(Integer, primary_key=True)
    origin = Column(String(255))
    destination = Column(String(255))
    departure = Column(TIMESTAMP)
    arrival = Column(TIMESTAMP)
    carrier = Column(String(255))
    vehicle_type = Column(String(255))
    price = Column(DECIMAL(10,2))
    currency = Column(String(3))
    source_id = Column(String(255))
    destination_id = Column(String(255))
    free_seats = Column(Integer)


