""" imports """
from flask import (Blueprint, 
        request, 
        jsonify, 
        render_template, 
        make_response)
from app.models.user import Users
from app.database.db import db 
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
import re 


# initate blueprint  
userRoute = Blueprint('user', __name__, url_prefix="/user")

""" autenticated user main page """
@userRoute.route('/protected', methods=['GET'])
@jwt_required()
def getProtected():
    return render_template('user/protected.html')

""" view profile cRud """
@userRoute.route("/profile", methods=['GET'])
@jwt_required()
def profile():
    # get current authenticated user from db 
    currentUser = Users.query.filter_by(id=get_jwt_identity()).first()
    # return template with current user's username and email 
    return render_template('user/profile.html', username=currentUser.username, email=currentUser.email)

""" delete user cruD """
@userRoute.route("/delete", methods=['DELETE'])
@jwt_required()
def deleteProfile():
    # find user we want to delete 
    currentUser = Users.query.filter_by(id=get_jwt_identity()).first()

    # specify basic msg and http code 
    msg = "User Does Not Exist"
    code = 400 

    if currentUser:
        try:
            # delete user from db 
            db.session.delete(currentUser)
            db.session.commit()

            msg = "Success."
            code = 200
        except Exception as e:
            print(e) # for logging 

            msg = "Unable to delete user."
            code = 500
    return make_response(msg, code)

""" update authenticated user information (email and/or username only) crUd """
@userRoute.route("/update", methods=['PUT'])
@jwt_required()
def updateProfile():
    # find current user 
    currentUser = Users.query.filter_by(id=get_jwt_identity()).first() 

    msg = "" 
    code = 200
    try:
        if request.method == 'PUT':
            formData = request.form
            newEmail = formData.get('email')
            newUsername = formData.get('username')
    except:
        # error intended for cURL or Postman 
        msg="Form read error."
        code = 400
        
    # check if another user with the same email exists in our db 
    userExist = Users.query.filter_by(email=newEmail).first() \
        if not (newEmail == currentUser.email) else None
    # check if another user with the same username exists in our db 
    usernameExist = Users.query.filter_by(username=newUsername).first() \
        if not (newUsername == currentUser.username) else None 

    if userExist or usernameExist:
        msg = "Username already in use." if not userExist else "Email already in use."
        code = 400
    elif not re.match(r"^\S+@\S+\.\S+$", newEmail):
        msg = "Please enter a valid email."
        code = 400 
    else:
        # add new user 
        try: 
            currentUser.username = newUsername
            currentUser.email = newEmail
            db.session.commit() 
        except: 
            msg = "Unable to update user information."
            code = 500
        
        msg = "User information updated." 
    return make_response(jsonify({"updateMsg":msg}), code)

""" protected route test """
@userRoute.route("/protected", methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user ID with get_jwt_identity 
    currentUserID = get_jwt_identity()
    return jsonify(logged_in_as=currentUserID), 200 
