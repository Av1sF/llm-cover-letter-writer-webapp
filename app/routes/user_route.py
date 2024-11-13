from flask import Blueprint, request, jsonify, render_template, make_response
from models.user import Users
from database.db import db 
from flask_jwt_extended import  get_jwt_identity
from flask_jwt_extended import jwt_required

import re 

userRoute = Blueprint('user', __name__, url_prefix="/user")

@userRoute.route('/protected', methods=['GET'])
@jwt_required()
def getProtected():
    return render_template('user/protected.html')


@userRoute.route("/profile", methods=['GET'])
@jwt_required()
def profile():
    currentUser = Users.query.filter_by(id=get_jwt_identity()).first()
    return render_template('user/profile.html', username=currentUser.username, email=currentUser.email)

@userRoute.route("/delete", methods=['DELETE'])
@jwt_required()
def deleteProfile():
    currentUser = Users.query.filter_by(id=get_jwt_identity()).first()
    response = "user does not exist"
    if currentUser:
        try:
            # db.session.delete(currentUser)
            # db.session.commit()
            response = make_response("Success")
        except Exception as e:
            print(e)
            # not the right code CORRECT 404 
            response = make_response("Unable to delete user.", 404)
    return response 

@userRoute.route("/update", methods=['PUT'])
@jwt_required()
def updateProfile():
    currentUser = Users.query.filter_by(id=get_jwt_identity()).first() 
    msg = "www" 
    if request.method == 'PUT':
        formData = request.form
        newEmail = formData.get('email')
        newUsername = formData.get('username')
        
    # check if the user with the same email exists in our db 
    userExist = Users.query.filter_by(email=newEmail).first() \
        if not (newEmail == currentUser.email) else None
    usernameExist = Users.query.filter_by(username=newUsername).first() \
        if not (newUsername == currentUser.username) else None 

    if userExist or usernameExist:
        msg = "Email already in use" if not userExist else "Username already in use"
    elif not re.match(r"^\S+@\S+\.\S+$", newEmail):
        msg = "Please enter a valid email"
    else:
        # add new user 
        try: 
            currentUser.username = newUsername
            currentUser.email = newEmail
            db.session.commit() 
        except: 
            msg = "Unable to update user information"
        
        msg = "User information updated"
    return make_response(jsonify({"msg":msg}), 200)
    # return render_template('auth/profile.html', updateMsg=msg) 

# Test Protected Route 
@userRoute.route("/protected", methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity 
    currentUser = get_jwt_identity()
    return jsonify(logged_in_as=currentUser), 200 
