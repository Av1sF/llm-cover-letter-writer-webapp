from database.db import db 

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40))
    username = db.Column(db.String(20))
    password = db.Column(db.String(255))

    def __init__(self, email, username, password) -> None:
        self.email = email
        self.password = password
        self.username = username 

    def __repr__(self):
        return f"{self.id}"