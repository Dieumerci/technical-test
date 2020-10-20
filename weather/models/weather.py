from ..app import db, app
from sqlalchemy.orm import relationship, configure_mappers, backref
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    Boolean,
    event,
    ARRAY,
    Date,
    Time,
    JSON
)
import datetime

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class WeatherModel(BaseModel, db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.String(50), nullable=False)
    temperature_min = db.Column(db.String(50), nullable=False)
    temperature_max = db.Column(db.String(50), nullable=False)
    humidity = db.Column(db.String(50), nullable=False)
    country_code = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), nullable=False)

    def __init__(self, name, description, temperature, temperature_min, temperature_max, humidity, country_code, icon):
        self.name = name
        self.description = description
        self.temperature = temperature
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.humidity = humidity
        self.country_code = country_code
        self.icon = icon

