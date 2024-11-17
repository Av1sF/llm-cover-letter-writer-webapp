""" imports """
from flask import Flask, render_template
from datetime import timedelta
from app.database import config 
from app.database.db import db 
from app.setup.jwt_setup import jwt 
from flask_sqlalchemy import SQLAlchemy 
from app.routes.auth_route import authRoute
from app.routes.user_route import userRoute
from app.routes.model_route import modelRoute

""" initalisations and configs """

# initalise flask app 
app = Flask(__name__, template_folder='templates', static_folder='static')

# config SQLAchemy from database/config.py 
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = True

# config JWT token cookies 
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# register routes from app/routes directory 
app.register_blueprint(modelRoute)
app.register_blueprint(authRoute)
app.register_blueprint(userRoute)

# initalise jwt with flask app from secure/jwt_setup.py 
jwt.init_app(app)

# initalise database with flask instance 
db.init_app(app)
with app.app_context(): 
    db.create_all()

""" Main page """
@app.route('/')
def home():
    return render_template("index.html"), 200 

if __name__ == "__main__":
    app.run(debug=True, port=5050)