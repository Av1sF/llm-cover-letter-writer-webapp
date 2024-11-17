""" imports """
from flask import (
    Blueprint, 
    request, 
    render_template, 
    make_response, 
    redirect)
from app.models.user import Users
from app.database.db import db 
from app.setup import password_hash
from flask_jwt_extended import (
    create_access_token, 
    set_access_cookies, 
    unset_jwt_cookies
    )
import re 

# initate blueprint 
authRoute = Blueprint('user_authentication', __name__, url_prefix="/auth")

""" serve login template """
@authRoute.route('/login', methods=['GET'])
def getLogin():
    response = render_template('auth/login.html'), 200 
    return response

""" serve register user template """
@authRoute.route('/register', methods=['GET'])
def getRegisted():
    response = render_template('auth/register.html'), 200 
    return response


""" create user Crud """
@authRoute.route('/register', methods=['POST'])
def createUser():
    try:
        if request.method == "POST":
            formEmail = request.form['email']
            formPassword = request.form['password']
            formUsername = request.form['username']

            # check if another user with the same email exists and/or username is in our db 
            usernameExist = Users.query.filter_by(username=formUsername).first()
            emailExist = Users.query.filter_by(email=formEmail).first()

            code = 400  # user errors 

            if emailExist and usernameExist:
                msg = "Both username and email already in use"
            elif emailExist or usernameExist:
                msg = "Email already in use" if emailExist else "Username already in use"
            elif not re.match(r"^\S+@\S+\.\S+$", formEmail):
                msg = "Please enter a valid email"
            elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", formPassword):
                # regex is for a password that has lower and uppercase letters, special characters, numbers, and atleast a length of 8
                msg = "Please enter a valid password"
            else:
                # add new user 
                try: 
                    newUser = Users(email=formEmail, password=password_hash.getPasswordHash(formPassword), username=formUsername)
                    db.session.add(newUser)
                    db.session.commit() 
                except: 
                    msg = "Unable to create user"
                    code = 500
                
                msg = "Created user successfully"
                code = 201     
        else:
            msg="Wrong method."
            code = 405 
    except:
        # error if wrong cURL request
        msg="Form read error."
        code = 400
    return render_template('auth/register.html', msg=msg), code


""" Log in user """
@authRoute.route('/login', methods=['POST'])
def createLoginToken(): 
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        # error incase of wrong cURL request 
        return render_template('auth/login.html', msg="Form read error."), 400

    # check if user is registered 
    userExist = Users.query.filter_by(username=username).first()

    if not userExist or not password_hash.verifyPassword(password, userExist.password):
        return render_template('auth/login.html', msg="Username or password is not correct"), 401
    else:
        try:
            # user is logged in and an access token is created, stored as a cookie 
            response = make_response(redirect('/user/protected'))
            access_token = create_access_token(identity=userExist.id)
            set_access_cookies(response, access_token)
            return response, 302 
        except Exception as e:
            return render_template('auth/login.html', msg="Server error."), 500

# Logout 
@authRoute.route("/logout", methods=['POST'])
def unsetTokenLogout():
    response = make_response(redirect('/'))
    unset_jwt_cookies(response)
    return response, 302 

