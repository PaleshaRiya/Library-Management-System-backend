from app.repositories.user_repository import UserRepository
from app.models.user import User
from flask_bcrypt import generate_password_hash, check_password_hash

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_all_users(self, filters=None):
        return self.user_repository.get_all_users(filters)

    def create_user(self, user_data):
        user = User(None, user_data['name'], user_data['username'], user_data['email'], True , user_data['password'], user_data['role'])
        user.password = generate_password_hash(user.password, 10)
        return self.user_repository.create_user(user)

    def update_user(self, user_id, user_data):
        existing_user = self.get_all_users({
            'id': user_id
        })[0]
        if not existing_user:
            raise ValueError("User not found")

        # Update only provided fields
        if 'name' in user_data:
            existing_user.name = user_data['name']
        if 'username' in user_data:
            existing_user.username = user_data['username']
        if 'email' in user_data:
            existing_user.email = user_data['email']
        if 'password' in user_data:
            existing_user.password = generate_password_hash(user_data['password'], 10)
        if 'role' in user_data:
            existing_user.role = user_data['role']
        if 'currentBooks' in user_data:
            existing_user.currentBooks = user_data['currentBooks']
        if 'active' in user_data:
            existing_user.active = user_data['active']

        self.user_repository.update_user(existing_user)

    def delete_user(self, user_id):
        self.user_repository.delete_user(user_id)
        
    def authenticate_user(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            return user
        return None
