import sqlite3
import os
from app.services import UserService

user_service = UserService()


def init_db():
    db_path = 'app/database.db'
    schema_path = 'app/schema.sql'

    # Check if the database file exists
    if not os.path.exists(db_path):
        connection = sqlite3.connect(db_path)

        # Execute the schema script if the database does not exist
        with open(schema_path) as f:
            connection.executescript(f.read())
            
        # Create an admin user
        user_service.create_user({
            'name' : 'admin',
            'username': 'admin',
            'password': 'admin',
            'email': 'admin@gmail.com',
            'role': 'ADMIN'
        })

        cur = connection.cursor()

        connection.commit()
        connection.close()
    else:
        print("Database already exists. Skipping schema execution.")
