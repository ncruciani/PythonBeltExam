from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from datetime import datetime
db = "exam"

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = User.get_by_id({'id': data['user_id']})


    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (price, model, make, year, description, user_id ) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result
    

    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s WHERE id = %(id)s;"
        connectToMySQL(db).query_db(query, data)
        return



    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        cars = []
        for row in results:
            cars_data = {
                'id': row['id'],
                'price': row['price'],
                'model': row['model'],
                'make': row['make'],
                'year': row['year'],
                'description': row['description'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password']
            }
            car = Car(cars_data)
            cars.append(car)
        return cars


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
    


    @staticmethod
    def validate_car(form_data):
        errors = []
        if len(form_data['price']) < 1:
            errors.append('price is requird.')
        if len(form_data['model']) < 1:
            errors.append('model is required.')
        if len(form_data['make']) < 1:
            errors.append('make is required.')
        if len(form_data['year']) < 1:
            errors.append('year is required.')
        if len(form_data['description']) < 1:
            errors.append('description is required.')
        return errors

