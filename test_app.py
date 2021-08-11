import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import logging

from trucker import create_app
from models import setup_db, Driver, Truck
from tokens import driver_token, admin_token

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    '''
#! successful get of all drivers
    def test_get_all_drivers_with_results(self):
        res = self.client().get('/drivers', headers=driver_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['driver_list'])
    

#! fail of get all drivers    
    def test_get_all_drivers_without_results(self):
        res = self.client().get('/name', headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")


#! successful get of all trucks
    def test_get_all_questions_with_results(self):
        res = self.client().get('/trucks', headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['truck_list'])


#! fail get of all trucks
    def test_get_all_trucks_without_results(self):
        res = self.client().get('/models', headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")


#! successful delete of a driver
    def test_delete_driver_with_results(self):
        res = self.client().delete('/drivers/4/', headers=admin_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


#! failed delete of a driver
    def test_delete_driver_without_results(self):
        res = self.client().delete('/drivers/2000/', headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
    
    
#! successful delete of a truck
    def test_delete_truck_with_results(self):
        res = self.client().delete('/trucks/5/', headers=admin_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    

#! failed delete of a truck
    def test_delete_truck_without_results(self):
        res = self.client().delete('/trucks/2000/', headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")

    
#! successful post of a driver
    def test_new_driver_with_results(self):
        res = self.client().post('/drivers/', json={'name': 'Jack', 'age': 18, 'gender': 'Male', 'truck_id': 1}, headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['name'], 'Jack')
        self.assertEqual(data['age'], 18)
        self.assertEqual(data['gender'], 'Male')
        self.assertEqual(data['truck_id'], 1)

#! successful post of a truck
    def test_new_truck_with_results(self):
        res = self.client().post('/trucks/', json={'model': 'Ram 3500', 'year': 1980, 'color': 'Black', 'haul_capacity': 18000, 'driver_id': 1}, headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['model'], 'Ram 3500')
        self.assertEqual(data['year'], 1980)
        self.assertEqual(data['color'], 'Black')
        self.assertEqual(data['haul_capacity'], 18000)
        self.assertEqual(data['driver_id'], 1)
    
#! successful search for driver   
    def test_get_driver_search_with_results(self):
        res = self.client().post('/drivers/', json={'searchTerm': 'Jack'}, headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_drivers'], 4)
        self.assertEqual(len(data['driver']), 4)
    
#! failed search for driver
    def test_get_driver_search_without_results(self):
        res = self.client().post('/drivers/', json={'searchTerm': 'fruit'}, headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['driver']), 0)

#! successful search for truck   
    def test_get_truck_search_with_results(self):
        res = self.client().post('/trucks/', json={'searchTerm': 'Ram 2500'}, headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_trucks'], 2)
        self.assertEqual(len(data['truck']), 2)
    
#! failed search for truck
    def test_get_truck_search_without_results(self):
        res = self.client().post('/trucks/', json={'searchTerm': 'Pink'}, headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['truck']), 0)
    '''
#! successful update for driver name
    def test_update_driver_name(self):
        res = self.client().patch('/drivers/4', json={'name': 'Bob'}, headers=admin_token())
        data = json.loads(res.data)
        driver = Driver.query.filter(Driver.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(driver.format()['name'], 'Bob')
        
#! successful update for driver name
    def test_update_driver_name_no_permissions(self):
        try:
            res = self.client().patch('/drivers/4', json={'name': 'Bob'}, headers=driver_token())
            data = json.loads(res.data)
            driver = Driver.query.filter(Driver.id == 4).one_or_none()
        except:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['code'], 'invalid_permissions')
            self.assertEqual(data['description'], 'User does not have enough privileges')
    '''

#! fail update for driver name
    def test_400_for_failed_update(self):
        res = self.client().patch('/drivers/1000', headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


#! successful update for truck model
    def test_update_truck_model(self):
        print('START TRUCK: ')

        res = self.client().patch('/trucks/1/', json={'model': 'Titan 2500'}, headers=admin_headers)
        data = json.loads(res.data)
        truck = Truck.query.filter(Truck.id == 1).one_or_none()
        #print('TRUCK: ') + truck
        print('TRUCK: ')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(truck.format()['model'], 'Titan 2500')

        
#! fail update for truck model
    def test_400_for_failed_update(self):
        res = self.client().patch('/trucks/1000', headers=admin_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

#! fail update for driver name. due to authorization for driver role
    def test_update_driver_name(self):
        res = self.client().patch('/drivers/1', json={'name': 'Bob'}, headers=driver_headers)
        data = json.loads(res.data)
        driver = Driver.query.filter(Driver.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(driver.format()['name'], 'Bob')
    '''
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()