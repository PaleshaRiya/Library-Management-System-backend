import sqlite3
from app.models.user import User

class UserRepository:
    def __init__(self):
        self.db_path = 'app/database.db'

    def get_all_users(self, filters=None):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        query = "SELECT id, name, username, email, active, password, role, currentBooks FROM user WHERE 1=1"
        params = []

        if filters:
            if 'username' in filters:
                query += " AND username = ?"
                params.append(filters['username'])
            if 'role' in filters:
                query += " AND role = ?"
                params.append(filters['role'])
            if 'email' in filters:
                query += " AND email = ?"
                params.append(filters['email'])
            if 'id' in filters:
                query += " AND id = ?"
                params.append(filters['id'])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        users = [User(*row) for row in rows]
        connection.close()
        return users

    def create_user(self, user):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user (name, username, email, password, role) VALUES (?, ?, ?, ?, ?)",
            (user.name, user.username, user.email, user.password, user.role)
        )
        connection.commit()
        user_id = cursor.lastrowid
        connection.close()
        return user_id

    def update_user(self, user):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE user SET name = ?, username = ?, email = ?, active = ?, password = ?, role = ?, currentBooks = ? WHERE id = ?",
            (user.name, user.username, user.email, user.active, user.password, user.role, user.currentBooks, user.id)
        )
        connection.commit()
        connection.close()

    def delete_user(self, user_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
        connection.commit()
        connection.close()

    def get_user_by_username(self, username):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, username, email,active, password, role FROM user WHERE username = ?", (username,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return User(*row)
        return None