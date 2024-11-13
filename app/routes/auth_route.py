from flask import Blueprint, request, jsonify, render_template, make_response, redirect, url_for, Response
from models.user import Users
from database.db import db 
from secure import password_hash
from secure.jwt_setup import jwt
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
import re 

authRoute = Blueprint('user_authentication', __name__, url_prefix="/auth")

# serve templates 
@authRoute.route('/login', methods=['GET'])
def getLogin():
    response = render_template('auth/login.html')
    return response

# @authRoute.route('/protected', methods=['GET'])
# @jwt_required()
# def getProtected():
#     return render_template('auth/protected.html')

@authRoute.route('/register', methods=['GET'])
def getRegisted():
    response = render_template('auth/register.html')
    return response


# Create user 
@authRoute.route('/register', methods=['POST'])
def createUser():
    msg = "" 
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']

    # check if the user with the same email exists in our db 
    userExist = Users.query.filter_by(email=email).first()
    usernameExist = Users.query.filter_by(username=username).first()

    if userExist or usernameExist:
        msg = "Email already in use" if not userExist else "Username already in use"
    elif not re.match(r"^\S+@\S+\.\S+$", email):
        msg = "Please enter a valid email"
    elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        msg = "Please enter a valid password"
    else:
        # add new user 
        try: 
            newUser = Users(email=email, password=password_hash.getPasswordHash(password), username=username)
            db.session.add(newUser)
            db.session.commit() 
        except: 
            msg = "Unable to create user"
        
        msg = "Created user successfully"

    return render_template('auth/register.html', msg=msg)
# Login user  
@authRoute.route('/login', methods=['POST'])
def createLoginToken(): 
    username = request.form['username']
    password = request.form['password']

    # check if the user with the same user exists in our db 
    userExist = Users.query.filter_by(username=username).first()
    if not userExist or not password_hash.verifyPassword(password, userExist.password):
        return "Username or password is not correct"
    else:
        try:
            response = make_response(redirect('/user/protected'))
            access_token = create_access_token(identity=userExist.id)
            set_access_cookies(response, access_token)
            return response
        except Exception as e:
            return e



# Logout 
@authRoute.route("/logout", methods=['POST'])
def unsetTokenLogout():
    response = make_response(redirect('/'))
    unset_jwt_cookies(response)
    return response

# @authRoute.route("/profile", methods=['GET'])
# @jwt_required()
# def profile():
#     currentUser = Users.query.filter_by(id=get_jwt_identity()).first()
#     return render_template('auth/profile.html', username=currentUser.username, email=currentUser.email)

# @authRoute.route("/delete", methods=['DELETE'])
# @jwt_required()
# def deleteProfile():
#     currentUser = Users.query.filter_by(id=get_jwt_identity()).first()
#     response = "user does not exist"
#     if currentUser:
#         try:
#             db.session.delete(currentUser)
#             db.session.commit()
#             response = redirect(url_for("user_authentication.getRegisted"), code=303)
#         except Exception as e:
#             print(e)
#             response = make_response("unable to create user")
#     return response 

# @authRoute.route("/update", methods=['PUT'])
# @jwt_required()
# def updateProfile():
#     currentUser = Users.query.filter_by(id=get_jwt_identity()).first() 
#     msg = "www" 
#     if request.method == 'PUT':
#         formData = request.form
#         newEmail = formData.get('email')
#         newUsername = formData.get('username')
        
#     # check if the user with the same email exists in our db 
#     userExist = Users.query.filter_by(email=newEmail).first() \
#         if not (newEmail == currentUser.email) else None
#     usernameExist = Users.query.filter_by(username=newUsername).first() \
#         if not (newUsername == currentUser.username) else None 

#     if userExist or usernameExist:
#         msg = "Email already in use" if not userExist else "Username already in use"
#     elif not re.match(r"^\S+@\S+\.\S+$", newEmail):
#         msg = "Please enter a valid email"
#     else:
#         # add new user 
#         try: 
#             currentUser.username = newUsername
#             currentUser.email = newEmail
#             db.session.commit() 
#         except: 
#             msg = "Unable to update user information"
        
#         msg = "User information updated"
#     return make_response(jsonify({"msg":msg}), 200)
#     # return render_template('auth/profile.html', updateMsg=msg) 

# # Test Protected Route 
# @authRoute.route("/protected", methods=['GET'])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity 
#     currentUser = get_jwt_identity()
#     return jsonify(logged_in_as=currentUser), 200 
