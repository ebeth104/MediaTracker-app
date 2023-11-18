from app.auth import db
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import (generate_password_hash,
                               check_password_hash)

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Check if the provided password matches the stored hash
        return check_password_hash(self.password_hash, password) 
    
    # def get_id(self):
    #     # Return the user ID as a string (required for Flask-Login)
    #     return str(self.id)

    
    def __repr__(self):
        return f'User {self.username}'
    
