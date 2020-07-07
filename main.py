#!/bin/python3
import sqlite3
from DataBaseManager import DBManager
import sys


db_path = "../../django_projects/carpricing/db.sqlite3"
django_db_connection = sqlite3.connect(db_path)
django_db_cursor = django_db_connection.cursor()
#? carbrand => id = 'id', Opel == 'name'
#? carmodel => id = 'id', Astra == 'name', car brand id = 'car_brand_id'

brands = DBManager.get_unique_brands_with_model()
for brand in brands:
    try:
        query = "SELECT id, name  FROM carpricing_carbrand WHERE name = '" + brand + "'"
        django_db_cursor.execute(query)
        brand_data = django_db_cursor.fetchall()
        brand_id_in_db = -1
        if (len(brand_data) == 0):
            insert_query = "INSERT INTO carpricing_carbrand(name) VALUES( +'" + brand + "')"
            django_db_cursor.execute(insert_query)
            brand_id_in_db = django_db_cursor.lastrowid
            django_db_connection.commit() 
        else:
            brand_id_in_db = brand_data[0][0]
        
        models = DBManager.get_unique_models_with_model(brand)
        for model in models:
            query = "SELECT id, name, car_brand_id FROM carpricing_carmodel WHERE name = '" + model + "' AND car_brand_id = '" + str(brand_id_in_db) + "'"
            django_db_cursor.execute(query)
            model_data = django_db_cursor.fetchall()
            if (len(model_data) == 0):
                insert_query = "INSERT INTO carpricing_carmodel(name, car_brand_id) VALUES( +'" + model + "', '" + str(brand_id_in_db) + "')"
                django_db_cursor.execute(insert_query)
                django_db_connection.commit() 
    except:
        print("Error", sys.exc_info()[0])
        

#             try:
                
#             except:
#                 print("Error", sys.exc_info()[0])

# c.execute("SELECT * FROM carpricing_carbrand")
# c.execute("SELECT * FROM carpricing_carmodel")
