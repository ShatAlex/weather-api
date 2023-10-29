from datetime import datetime

from sqlalchemy import MetaData, Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base

metadata = MetaData()


class City(Base):
    __tablename__ = "cities"

    id: int = Column(Integer, primary_key=True)
    city_name: str = Column(String, nullable=False)
    weathers = relationship('Weather')


class Weather(Base):
    __tablename__ = "weathers"

    id: int = Column(Integer, primary_key=True)
    temperature: int = Column(Integer, nullable=False)
    pressure: int = Column(Integer, nullable=False)
    wind: float = Column(Float, nullable=False)
    date: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    city = Column(Integer, ForeignKey('cities.id'))
