from sqlalchemy import Column, String, Integer, create_engine, Table, ForeignKey
from flask_sqlalchemy import SQLAlchemy

database_name = "capstone"
database_name = "capstone_test"
database_path = "postgresql://postgres:postgres@{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
    db.create_all()

'''
Trucks
'''
class Truck(db.Model):
    __tablename__ = 'truck'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    model = Column(String)
    color = Column(String)
    haul_capacity = Column(Integer)
    driver_id = Column(Integer, db.ForeignKey('driver.id'))

    def __init__(self, year, model, color, haul_capacity, driver_id):
        self.year = year
        self.model = model
        self.color = color
        self.haul_capacity = haul_capacity
        self.driver_id = driver_id

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'year': self.year,
          'model': self.model,
          'color': self.color,
          'haul_capacity': self.haul_capacity,
          'driver_id': self.driver_id
        }

'''
Driver
'''
class Driver(db.Model):
    __tablename__ = 'driver'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    gender = Column(String)
    truck_id = Column(Integer, db.ForeignKey('truck.id'))

    def __init__(self, name, age, gender, truck_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.truck_id = truck_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'truck_id': self.truck_id,
        }
