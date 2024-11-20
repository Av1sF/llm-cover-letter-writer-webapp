""" imports """
from flask import (Blueprint, 
        request, 
        jsonify, 
        render_template, 
        make_response)
from models.user import Users
from database.db import db 
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
    return render_template('user/protected.html'), 200

""" view profile cRud """
@userRoute.route("/profile", methods=['GET'])
@jwt_required()
def profile():
    # get current authenticated user from db 
    currentUser = Users.query.filter_by(id=get_jwt_identity()).first()
    # return template with current user's username and email 
    return render_template('user/profile.html', username=currentUser.username, email=currentUser.email), 200 

""" delete user cruD """
@userRoute.route("/delete", methods=['DELETE'])
@jwt_required()
def deleteProfile():
    # find user we want to delete 
    currentUser = Users.query.filter_by(id=get_jwt_identity()).first()

    # specify basic msg and http code 
    msg, code = "User Does Not Exist", 400 

    if currentUser:
        try:
            # delete user from db 
            db.session.delete(currentUser)
            db.session.commit()

            msg = "Success."
            code = 204
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
    code = None
    
    try:
        newUsername = request.form.get('username')
        newEmail = request.form.get('email')

        if newUsername or newEmail:
            # check if another user with the same email exists in our db 
            emailExist = Users.query.filter_by(email=newEmail).first() \
                if not (newEmail == currentUser.email) else None
            # check if another user with the same username exists in our db 
            usernameExist = Users.query.filter_by(username=newUsername).first() \
                if not (newUsername == currentUser.username) else None 

            if emailExist or usernameExist:
                msg = "Username already in use." if usernameExist else "Email already in use."
                code = 400
            elif newEmail and (not re.match(r"^\S+@\S+\.\S+$", newEmail)):
                msg = "Please enter a valid email."
                code = 400 
            else:
                # add new user 
                try:
                    if newUsername:
                        currentUser.username = newUsername
                    if newEmail:
                        currentUser.email = newEmail
                    db.session.commit() 
                except: 
                    msg = "Unable to update user information."
                    code = 500
                
                msg = "User information updated." 
                code = 200
        else:
            raise Exception
    except Exception as e:
        # error intended for cURL or Postman 
        msg="Form read error."
        code = 400

    return make_response(jsonify({"updateMsg":msg}), code)
