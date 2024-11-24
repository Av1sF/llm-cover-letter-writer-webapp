import sys
sys.path.append('app')
from database.db import db 

class Users(db.Model):
    __tablename__ = "users"
    
    # columns 
    id = db.Column(db.Integer, primary_key=True, extend_existing=True)
    email = db.Column(db.String(40), extend_existing=True)
    username = db.Column(db.String(20), extend_existing=True)
    password = db.Column(db.String(255), extend_existing=True)
    
    def __init__(self, email, username, password) -> None:
        self.email = email
        self.password = password
        self.username = username 

    def __repr__(self):
        return f"{self.id}"