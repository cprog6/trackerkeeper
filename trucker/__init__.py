from flask import Flask, json, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Driver, Truck
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  #GET ALL DRIVERS
  @app.route('/drivers', methods=['GET'])
  @requires_auth('get:drivers')
  def get_drivers(f):
    drivers = Driver.query.all()
    formatted_drivers = [driver.format() for driver in drivers]
    
    name_list = []
    for driver in drivers:
      name_list.append(driver.name)
    
    return jsonify({
      'success': True,
      'driver_list': formatted_drivers,
      'name_list': name_list
      })
  
  #GET ALL TRUCKS
  @app.route('/trucks', methods=['GET'])
  @requires_auth('get:trucks')
  def get_trucks(f):
    trucks = Truck.query.all()
    formatted_trucks = [truck.format() for truck in trucks]

    return jsonify({
      'success': True,
      'truck_list': formatted_trucks,
      })

  
  #CREATE OR SEARCH FOR DRIVERS
  @app.route('/drivers/', methods=['POST'])
  @requires_auth('post:drivers')
  def create_or_search_drivers(f):
    try:
      body = request.get_json()
      search_term = body.get('searchTerm', None)

      if search_term == None:
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        new_truck_id = body.get('truck_id', None)

        driver_record = Driver(name=new_name, age=new_age, gender=new_gender, truck_id=new_truck_id)

        driver_record.insert()
        
        return jsonify({
          'success': True,
          'name': new_name,
          'age': new_age,
          'gender': new_gender,
          'truck_id': new_truck_id
        })

      else:
        driver_list = Driver.query.filter(Driver.name.ilike(f'%{search_term}%')).all()

        formatted_driver = [driver.format() for driver in driver_list]
        
        return jsonify({
          'success': True,
          'driver':formatted_driver,
          'total_drivers':len(formatted_driver)
        })       

    except Exception as e:
      app.logger.warning(e)
      abort(422)
  
  #CREATE OR SEARCH FOR TRUCKS
  @app.route('/trucks/', methods=['POST'])
  @requires_auth('post:trucks')
  def create_or_search_trucks(f):
    try:
      body = request.get_json()
      search_term = body.get('searchTerm', None)

      if search_term == None:
        new_year = body.get('year', None)
        new_model = body.get('model', None)
        new_color = body.get('color', None)
        new_haul_capacity = body.get('haul_capacity', None)
        new_driver_id = body.get('driver_id', None)

        truck_record = Truck(year=new_year, model=new_model, color=new_color, haul_capacity=new_haul_capacity, driver_id=new_driver_id)

        truck_record.insert()
        
        return jsonify({
          'success': True,
          'year': new_year,
          'model': new_model,
          'color': new_color,
          'haul_capacity': new_haul_capacity,
          'driver_id': new_driver_id
        })

      else:
        truck_list = Truck.query.filter(Truck.model.ilike(f'%{search_term}%')).all()
        formatted_truck = [truck.format() for truck in truck_list]
        
        return jsonify({
          'success': True,
          'truck':formatted_truck,
          'total_trucks':len(formatted_truck)
        })       

    except Exception as e:
      app.logger.warning(e)
      abort(422)
  
  #DELETE TRUCK
  @app.route('/trucks/<int:truck_id>/', methods=['DELETE'])
  @requires_auth('delete:trucks')
  def delete_trucks(f, truck_id):

    truck = Truck.query.filter(Truck.id == truck_id).one_or_none()
    if truck is None:
      abort(404)

    try:  
      truck.delete()
      
      return jsonify({
        'success': True,
      })

    except:
      abort(422)
  
  #DELETE DRIVER
  @app.route('/drivers/<int:driver_id>/', methods=['DELETE'])
  #@requires_auth('delete:drivers')
  def delete_driver(driver_id):

    driver = Driver.query.filter(Driver.id == driver_id).one_or_none()
    print("driver: {}".format(driver.name))
    if driver is None:
      abort(404)

    try:  
      driver.delete()
      
      return jsonify({

        'success': True,

      })

    except:
      abort(422)

  
  #UPDATE A TRUCK RECORD
  @app.route('/trucks/<int:truck_id>/', methods=['PATCH'])
  @requires_auth('patch:trucks')
  def update_truck(f, truck_id):
    print("truck update: ")
    body = request.get_json()

    try:
      truck = Truck.query.filter(Truck.id == truck_id).one_or_none()
      if truck is None:
        abort(404)

      if 'year' in body:
        truck.year = int(body.get('year'))

      if 'model' in body:
        truck.model = str(body.get('model'))

      if 'color' in body:
        truck.color = str(body.get('color'))

      if 'haul_capacity' in body:
        truck.haul_capacity = int(body.get('haul_capacity'))

      if 'driver_id' in body:
        truck.driver_id = int(body.get('driver_id'))

      truck.update()

      return jsonify({
        'success': True,
      })
    
    except:
      abort(400)
  
  #UPDATE A DRIVER RECORD
  @app.route('/drivers/<int:driver_id>', methods=['PATCH'])
  @requires_auth('patch:drivers')
  def update_driver(f, driver_id):
    body = request.get_json()

    try:
      driver = Driver.query.filter(Driver.id == driver_id).one_or_none()
      if driver is None:
        abort(404)

      if 'name' in body:
        driver.name = str(body.get('name'))
      
      if 'age' in body:
        driver.age = int(body.get('age'))

      if 'gender' in body:
        driver.gender = str(body.get('gender'))

      if 'truck_id' in body:
        driver.truck_id = int(body.get('truck_id'))
      
      driver.update()

      return jsonify({
        'success': True,
      })
      
    except:
      abort(400)
  

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,  
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  return app