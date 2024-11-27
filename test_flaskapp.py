""" imports """
import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# flask app instance and test client 
from app.app import app 
import pytest 
import responses 


""" 
Run test by 'pytest' in powershell. ETA: 3.58 seconds 

"""

# global variables (user authentication)
accessTokenCookie = None 
csrfAccessToken = None 

# set up
@pytest.fixture 
def client():
    """ A test client for the app """
    with app.test_client() as client:
        try:
            # create a test user 
            response = client.post("auth/register", data={"username":"testing123", 
                                                  "email" : "testing123@gmail.com", 
                                                  "password": "testingONLY111!"})
            assert response.status_code == 201
            assert b"Created user successfully" in response.data
        except:
            # user already exists 
            pass 

        yield client 

''' 

app.py tests 

'''
def testHome(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is retrieved
    THEN check it returns the main page template
    """
    response = client.get("/")
    
    assert response.status_code == 200 
    assert b"<title>Cover Letter Writer. </title>" in response.data 

''' 

auth route tests 

'''
def testLoginTemplate(client):
    """
    Normal Data
    GIVEN a Flask application configured for testing
    WHEN the 'auth/login' page is retrieved
    THEN check it returns the login template
    """
    response = client.get("auth/login")
    
    assert response.status_code == 200 
    assert b"<title>Login</title>" in response.data 

# Creating new users (auth/register)

def testRegisterTemplate(client):
    """
    Normal Data
    GIVEN a Flask application configured for testing
    WHEN the 'auth/register' page is retrieved
    THEN check it returns the register template
    """
    response = client.get("auth/register")

    assert response.status_code == 200 
    assert b"<title>Register</title>" in response.data 

def testRegisterTakenUsername(client):
    """
    Erroneous Data 
    GIVEN a taken username 
    WHEN a new user wants to register 
    THEN check that the html displays that the "username already is use" 
    """
    # use our test user's username 
    response = client.post("auth/register", data={"username":"testing123", 
                                                  "email" : "randommeeprandom@gmail.com", 
                                                  "password": "wefkfopkfL2004!"})
    assert response.status_code == 400 
    assert b"Username already in use" in response.data

def testRegisterTakenEmail(client):
    """
    Erroneous Data 
    GIVEN a taken email 
    WHEN a new user is wants to register 
    THEN check that the html displays that the "email already is use" 
    """
    # use our test user's email
    response = client.post("auth/register", data={"username":"randomrandomrewdqwqwewandom", 
                                                  "email" : "testing123@gmail.com", 
                                                  "password": "wefkfopkfL2004!"})
    assert response.status_code == 400 
    assert b"Email already in use" in response.data

def testRegisterTakenEmailUsername(client):
    """
    Erroneous Data 
    GIVEN a taken email and username 
    WHEN a new user attempts to register
    THEN check that the html displays that the "Both username and email already in use" 
    """
    # use our test user's email and username 
    response = client.post("auth/register", data={"username":"testing123", 
                                                  "email" : "testing123@gmail.com", 
                                                  "password": "wefkfopkfL2004!"})
    assert response.status_code == 400 
    assert b"Both username and email already in use" in response.data

def testRegisterInvalidEmail(client):
    """
    Handling Erroneous Data 

    GIVEN a invalid email 
    WHEN a new user attempts to register
    THEN check that the html displays that the "Please enter a valid email" 
    """
    response = client.post("auth/register", data={"username":"randomrandomrandom", 
                                                  "email" : "meowAT!gmail>com", 
                                                  "password": "wefkfopkfL2004!"})
    assert response.status_code == 400 
    assert b"Please enter a valid email" in response.data

def testRegisterInvalidPassword(client):
    """
    Erroneous Data 
    GIVEN a invalid password  
    WHEN a new user attempts to register
    THEN check that the html displays that the "Please enter a valid password" 
    """
    response = client.post("auth/register", data={"username":"randomrandomrandom", 
                                                  "email" : "meow234drandom@gmail.com", 
                                                  "password": "!"})
    assert response.status_code == 400 
    assert b"Please enter a valid password" in response.data

def testRegisterInvalidForm(client):
    """
    Handling Erroneous Data 

    GIVEN a taken invalid form from client 
    WHEN a new user attempts to register 
    THEN check that response states that there is a form error 
    """
    # wrong keys  
    response = client.post("auth/register", data={"username":"testy1", 
                                                  "meow" : "randomrandom@gmail.com", 
                                                  "password": "wefkfopkfL2004!"})
    assert response.status_code == 400
    assert b"Form read error." in response.data

    # missing keys  
    response = client.post("auth/register", data={"username":"testy1",  
                                                  "password": "wefkfopkfL2004!"})
    assert response.status_code == 400
    assert b"Form read error." in response.data

    # no data 
    response = client.post("auth/register")
    assert response.status_code == 400
    assert b"Form read error." in response.data

def testRegisterUser(client):
    """
    Normal Data 
    GIVEN valid password, username and email 
    WHEN a new user attempts to register 
    THEN should return a response that says "Created user successfully" 
    """
    # create another test user 
    response = client.post("auth/register", data={"username":"testingONLY", 
                                                  "email" : "testingONLY@gmail.com", 
                                                  "password": "testingONLY111!"})
    assert response.status_code == 201
    assert b"Created user successfully" in response.data

# User Login (auth/login)

def testLoginInvalidForm(client):
    """
    Erroneous Data 
    GIVEN a invalid form from client 
    WHEN a user attempts to login 
    THEN check that response states that there is a form error 
    """
    # wrong keys 
    response = client.post("auth/login", data={"username":"testy1", 
                                                  "meow" : "wefkfopkfL2004!"})
    assert response.status_code == 400
    assert b"Form read error." in response.data

    # no submitted data 
    response = client.post("auth/login")
    assert response.status_code == 400
    assert b"Form read error." in response.data

    # missing keys 
    response = client.post("auth/login", data={"password" : "wefkfopkfL2004!"})
    assert response.status_code == 400
    assert b"Form read error." in response.data

def testLoginInvalidUsername(client):
    """
    Erroneous Data 
    GIVEN a non-registered username from client 
    WHEN a user is attempts to login 
    THEN check that response states that the "Username or password is not correct"
    """
    response = client.post("auth/login", data={"username":"!!@#$#$#%^^&@#", 
                                                  "password" : "wefkfopkfL2004!"})
    assert response.status_code == 401
    assert b"Username or password is not correct" in response.data

def testLoginInvalidPassword(client):
    """
    Erroneous Data 
    GIVEN a wrong password from client 
    WHEN a user is attempts to login  
    THEN check that response states that the "Username or password is not correct"
    """
    response = client.post("auth/login", data={"username":"testingONLY", 
                                                  "password" : "wrongpassword"})
    assert response.status_code == 401
    assert b"Username or password is not correct" in response.data

def testValidLogin(client): 
    """
    Normal Data 
    GIVEN a correct registered username and password 
    WHEN a user attempts to login 
    THEN check that response is a redirect (302) and it returns the access token and csrf token 
    """
    response = client.post("auth/login", data={"username":"testingONLY", 
                                                  "password": "testingONLY111!"})
    
    assert response.status_code == 302
    assert len(response.headers.getlist('Set-Cookie')) == 2
    assert response.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[0] == "access_token_cookie"
    assert response.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[0] == "csrf_access_token"

# User Logout (auth/logout)

def testValidLogout(client):
    """
    Normal Data 
    GIVEN a user
    WHEN the user posts to /logout 
    THEN check that response is a redirect (302) and any tokens are expired  
    """
    response = client.post("auth/logout")

    assert response.status_code == 302 
    # check if all tokens stored in the cookies are expired 
    cookieExpiry = [c.split(";")[1] for c in response.headers.getlist('Set-Cookie')]
    assert cookieExpiry == ([' Expires=Thu, 01 Jan 1970 00:00:00 GMT'] * len(response.headers.getlist('Set-Cookie')))


'''  

user route tests 

'''

# protected main page (user/protected)

def testUnauthProtectedPage(client):
    """
    Erroneous Data 
    GIVEN a user that is NOT logged in 
    WHEN the user tries to retrieve a JWT protected page 
    THEN check that response states that it is unauthorised (401)
    """
    response = client.get("user/protected")
    assert response.status_code == 401 
 
def testProtectedPage(client):
    """
    Normal Data 
    GIVEN a user that is logged in 
    WHEN the user tries to retrieve a JWT protected page 
    THEN check that response serves the correct template 
    """
    global accessTokenCookie
    global csrfAccessToken

    # log in to our test user 
    loginResponse = client.post("auth/login", data={"username":"testingONLY", 
                                                  "password": "testingONLY111!"})
    # retrieve tokens 
    accessTokenCookie = loginResponse.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1] 
    csrfAccessToken = loginResponse.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1] 

    # send get request with access token 
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)
    response = client.get("user/protected")

    # log in 
    assert loginResponse.status_code == 302
    assert len(loginResponse.headers.getlist('Set-Cookie')) == 2
    assert loginResponse.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[0] == "access_token_cookie"
    assert loginResponse.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[0] == "csrf_access_token"

    # retrieving protected page 
    assert response.status_code == 200 
    assert b"<h1>Generate your cover letter!</h1>" in response.data

# profile page (user/profile)

def testUnauthProfilePage(client):
    """
    Erroneous Data 
    GIVEN a user that is NOT logged in 
    WHEN the user tries to retrieve a JWT required page to view profile
    THEN check that response states that it is unauthorised request (401)
    """
    response = client.get("user/profile")
    assert response.status_code == 401 

def testProfilePage(client):
    """
    Normal Data 
    GIVEN a user that is logged in 
    WHEN the user tries to retrieve a JWT required page to view their profile
    THEN check that response serves the correct template featuring user's username and email
    """
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)
    response = client.get("user/profile")

    assert response.status_code == 200 
    # check that it is logged into the right user 
    assert b"testingONLY" in response.data
    assert b"testingONLY@gmail.com" in response.data 

# update user information (user/update)
def testUnauthUserUpdate(client):
    """
    Erroneous Data 
    GIVEN a user that is not logged in
    WHEN the user tries to update their username and/or email 
    THEN check that response states that is unauthorised (401)
    """
    # correct data  
    response = client.put("user/update", data={
        "email" : "test123emailchange@gmail.com",
        "username" : "newusernametest123"
    })
    assert response.status_code == 401

    # no data submitted 
    response = client.put("user/update")
    assert response.status_code == 401

    # wrong key in data 
    response = client.put("user/update", data={
        "email" : "test123emailchange@gmail.com",
        "WrongKey" : "newusernametest123"
    })
    assert response.status_code == 401

    # missing keys 
    response = client.put("user/update", data={
        "username" : "newusernametest123"
    })
    assert response.status_code == 401

def testUnauthCSRFUserUpdate(client):
    """
    Erroneous Data 
    GIVEN a user that is logged in but has not attached CSRF-TOKEN in their PUT request
    WHEN the user tries to update their username and/or email 
    THEN check that response states that is unauthorised (401)
    """
    # set access token 
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    # correct data 
    response = client.put("user/update", data={
        "email" : "test123emailchange@gmail.com",
        "username" : "newusernametest123"
    })
    # unauthorised because no csrf token in header 
    assert response.status_code == 401

    # no data submitted 
    response = client.put("user/update")
    assert response.status_code == 401

    # wrong key in data 
    response = client.put("user/update", data={
        "email" : "test123emailchange@gmail.com",
        "WrongKey" : "newusernametest123"
    })
    assert response.status_code == 401

    # missing keys 
    response = client.put("user/update", data={
        "username" : "newusernametest123"
    })
    assert response.status_code == 401

def testUnauthAccessUserUpdate(client): 
    """
    Erroneous Data 
    GIVEN a user has no access token in cookies but has attached CSRF token in their request headers 
    WHEN the user tries to update their username and/or email 
    THEN check that response states that is unauthorised (401)
    """
    # normal data 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "email" : "testingONLYemailchange@gmail.com",
                            "username" : "newusernametestingONLY"
                        })
    # unauthorised because no access token in cookies 
    assert response.status_code == 401

    # wrong keys 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "emWRONGail" : "testingONLYemailchange@gmail.com",
                            "username" : "newusernametestingONLY"
                        }) 
    assert response.status_code == 401

    # no data 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken})
    assert response.status_code == 401

    # missing keys 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "email" : "testingONLYemailchange@gmail.com",
                        })
    assert response.status_code == 401

def testInvalidFormUpdateUser(client): 
    """
    Erroneous Data 
    GIVEN a user that is logged in and has attached CSRF token
    WHEN the user tries to update their details with an invalid form
    THEN check that response states a form read error 
    """
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    # no data attached 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          )
    assert response.status_code == 400
    assert b"Form read error." in response.data 

    # wrong keys 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "emeeail" : "test123emailchange@gmail.com",
                            "error" : "nonvalidfieldused",
                        })
    assert response.status_code == 400
    assert b"Form read error." in response.data 
    # TODO: NEED TO ADD MORE TEST ONE  USERNAME FIELD ONE DK FEIELD SHOULD REJECT 

def testTakenUsernameUpdateUser(client):
    """
    Erroneous Data 

    GIVEN a user that is logged in and has attached CSRF token
    WHEN the user tries to update their details with a username that is already in use
    THEN check that response states that the username is already in use 
    """
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    # only update username 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                              "username": "testing123", 
                          })
    assert response.status_code == 400
    assert b"Username already in use." in response.data 

    # update username and password 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "username":"testing123",
                            "email" : "randomran12f0+32f@gmail.com"
                        })
    assert response.status_code == 400
    assert b"Username already in use." in response.data 

def testTakenEmailUpdateUser(client):
    """
    Erroneous Data 
    GIVEN a user that is logged in and has attached CSRF token
    WHEN the user tries to update their details with a email that is already in use
    THEN check that response states that the email is already in use 
    """
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    # only update email 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                              "email": "testing123@gmail.com",
                          })
    assert response.status_code == 400
    assert b"Email already in use." in response.data 

    # update email and username 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "username":"testingONLY",
                            "email": "testing123@gmail.com",
                        })
    assert response.status_code == 400
    assert b"Email already in use." in response.data

def testInvalidEmailUpdateUser(client):
    """
    Erroneous Data 
    GIVEN a user that is logged in and has attached CSRF token
    WHEN the user tries to update their details with an invalid email in a valid form
    THEN check that response states that the email is invalid 
    """
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    # only update email 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                              "email": "testing123AT!!gmail.com",
                          })
    assert response.status_code == 400
    assert b"Please enter a valid email." in response.data 

    # update email and username 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "username":"testingONLY",
                            "email": "testing123AT!!gmail.com",
                        })
    assert response.status_code == 400
    assert b"Please enter a valid email." in response.data

def testValidUserUpdate(client):
    """
    Normal Data 
    GIVEN a user that is logged in and has attached CSRF token
    WHEN the user tries to update their details with a valid form
    THEN check that response states user information is updated 
    """

    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    # only email
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                              "email": "testingONLYEMAIL_CHANGE@gmail.com",
                          })
    assert response.status_code == 200
    assert b"User information updated." in response.data 

    # only username
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "username":"testingChangeonly",
                        })
    assert response.status_code == 200
    assert b"User information updated." in response.data 

    # both 
    response = client.put("user/update", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken},
                          data={
                            "username":"testingONLYchange",
                            "email":"testingONLYchange@gmail.com"
                        })
    assert response.status_code == 200
    assert b"User information updated." in response.data 

# delete user information (user/delete)
def testUnauthRequestUserDelete(client):
    """
    Erroneous Data 
    GIVEN a user that is logged in but has not attached CSRF-TOKEN in their request
    WHEN the user tries to delete their user account 
    THEN check that response states that is unauthorised
    """
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    response = client.delete("user/delete")

    # unauthorised because no csrf token in header 
    assert response.status_code == 401

def testUnauthAccessUserDelete(client): 
    """
    Erroneous Data 
    GIVEN a user that is NOT logged in but has attached CSRF-TOKEN in their request
    WHEN the user tries to delete their user account 
    THEN check that response states that is unauthorised
    """
    response = client.delete("user/delete", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken})

    # unauthorised because no access token in cookies 
    assert response.status_code == 401

def testValidUserDelete(client): 
    """
    Normal Data 
    GIVEN a user that is logged in and has attached CSRF-TOKEN in their request
    WHEN the user tries to delete their user account 
    THEN check that response status code shows user resource is deleted 
    """
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    response = client.delete("user/delete", 
                          headers= {"X-CSRF-TOKEN": csrfAccessToken})
 
    assert response.status_code == 204

'''

model route tests 

'''
# querying model (model/query)

def testUnauthQueryModel(client):
    """
    Erroneous Data 
    GIVEN a user that is NOT logged in 
    WHEN the user tries to query the model 
    THEN check that response states that it is unauthorised  
    """
    # no data 
    response = client.post("model/query")
    assert response.status_code == 401 

    # correct data 
    response = client.post("model/query", data={
        "Job Title" : "Data Scientist", 
        "Preferred Qualifications" : """BSc focused on data Science/computer Science/engineering
        4+ years experience Developing and shipping production grade machine learning systems
        2+ years building and shipping data Science based personalization services and recommendation systems
        experience in data Science or machine learning engineering
        Strong analytical and data Science skills""",
        "Hiring Company" : "XYZ Corporation", 
        "Applicant Name" : "John Smith", 
        "Past Working Experience" : "Data Analyst at ABC Company",
        "Current Working Experience" : "Machine Learning Engineer at DEF Company",
        "Skillsets" : "Python, R, scikit-learn, Keras, Tensorflow",
        "Qualifications" : "BSc in Computer Science, 5+ years of experience in data science and machine learning",
    })
    assert response.status_code == 401 

def testUnauthCSRFQueryModel(client):
    """
    Erroneous Data 
    GIVEN a user that is logged in but has not attached the CSRF token in request 
    WHEN the user tries to query the model 
    THEN check that response states that it is unauthorised  
    """
    global accessTokenCookie
    global csrfAccessToken
    # log in to test user 
    loginResponse = client.post("auth/login", data={"username":"testing123", 
                                                  "password": "testingONLY111!"})
    # retrieve tokens 
    accessTokenCookie = loginResponse.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[1] 
    csrfAccessToken = loginResponse.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[1] 

    # log in assertations 
    assert loginResponse.status_code == 302
    assert len(loginResponse.headers.getlist('Set-Cookie')) == 2
    assert loginResponse.headers.getlist('Set-Cookie')[0].split(";")[0].split("=")[0] == "access_token_cookie"
    assert loginResponse.headers.getlist('Set-Cookie')[1].split(";")[0].split("=")[0] == "csrf_access_token"

    # set access token 
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    # correct data 
    response = client.post("model/query", data={
        "Job Title" : "Data Scientist", 
        "Preferred Qualifications" : """BSc focused on data Science/computer Science/engineering
        4+ years experience Developing and shipping production grade machine learning systems
        2+ years building and shipping data Science based personalization services and recommendation systems
        experience in data Science or machine learning engineering
        Strong analytical and data Science skills""",
        "Hiring Company" : "XYZ Corporation", 
        "Applicant Name" : "John Smith", 
        "Past Working Experience" : "Data Analyst at ABC Company",
        "Current Working Experience" : "Machine Learning Engineer at DEF Company",
        "Skillsets" : "Python, R, scikit-learn, Keras, Tensorflow",
        "Qualifications" : "BSc in Computer Science, 5+ years of experience in data science and machine learning",
    })
    # no CSRF token in headers 
    assert response.status_code == 401 

    # no data 
    response = client.post("model/query")
    assert response.status_code == 401 

def testUnauthAccessQueryModel(client):
    """
    Erroneous Data 
    GIVEN a user that has attached the CSRF token in request but has not set the Access Token cookie 
    WHEN the user tries to query the model 
    THEN check that response states that it is unauthorised  
    """
    # correct data 
    response = client.post("model/query", 
        headers= {"X-CSRF-TOKEN": csrfAccessToken},
        data={
        "Job Title" : "Data Scientist", 
        "Preferred Qualifications" : """BSc focused on data Science/computer Science/engineering
        4+ years experience Developing and shipping production grade machine learning systems
        2+ years building and shipping data Science based personalization services and recommendation systems
        experience in data Science or machine learning engineering
        Strong analytical and data Science skills""",
        "Hiring Company" : "XYZ Corporation", 
        "Applicant Name" : "John Smith", 
        "Past Working Experience" : "Data Analyst at ABC Company",
        "Current Working Experience" : "Machine Learning Engineer at DEF Company",
        "Skillsets" : "Python, R, scikit-learn, Keras, Tensorflow",
        "Qualifications" : "BSc in Computer Science, 5+ years of experience in data science and machine learning",
    })
    assert response.status_code == 401 

    # no data 
    response = client.post("model/query", 
                           headers= {"X-CSRF-TOKEN": csrfAccessToken})
    assert response.status_code == 401 

def testInvalidFormQueryModel(client):
    """
    Erroneous Data 
    GIVEN a logged in user 
    WHEN the user tries to query the model with an invalid form  
    THEN check that response states that there is a form read error   
    """
    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    # missing json keys  
    response = client.post("model/query", 
        headers= {"X-CSRF-TOKEN": csrfAccessToken},
        data={
        "Job Title" : "Data Scientist", 
        "Preferred Qualifications" : """BSc focused on data Science/computer Science/engineering
        4+ years experience Developing and shipping production grade machine learning systems
        2+ years building and shipping data Science based personalization services and recommendation systems
        experience in data Science or machine learning engineering
        Strong analytical and data Science skills""",
        "Hiring Company" : "XYZ Corporation", 
        "Applicant Name" : "John Smith", 
        "Past Working Experience" : "Data Analyst at ABC Company",
    })
    assert response.status_code == 400
    assert b"Form read error." in response.data 

    # request with no data 
    response = client.post("model/query", 
        headers={"X-CSRF-TOKEN": csrfAccessToken})
    assert response.status_code == 400
    assert b"Form read error." in response.data  

    # form with right number of keys but wrong key names 
    response = client.post("model/query", 
        headers= {"X-CSRF-TOKEN": csrfAccessToken},
        data={
        "Job TitleWRONG" : "Data Scientist", 
        "PreferredWRONG Qualifications" : """BSc focused on data Science/computer Science/engineering
        4+ years experience Developing and shipping production grade machine learning systems
        2+ years building and shipping data Science based personalization services and recommendation systems
        experience in data Science or machine learning engineering
        Strong analytical and data Science skills""",
        "Hiring Company" : "XYZ Corporation", 
        "Applicant WRONGName" : "John Smith", 
        "Past Working Experience" : "Data Analyst at ABC Company",
        "CurreWRONGt Working Experience" : "Machine Learning Engineer at DEF Company",
        "Skillsets" : "Python, R, scikit-learn, Keras, Tensorflow",
        "QualificatWRONGions" : "BSc in Computer Science, 5+ years of experience in data science and machine learning",
    })
    assert response.status_code == 400
    assert b"Form read error." in response.data  
    
    # form with all valid keys but with 2 extra keys  
    response = client.post("model/query", 
        headers= {"X-CSRF-TOKEN": csrfAccessToken},
        data={
        "Job Title" : "Data Scientist", 
        "Preferred Qualifications" : """BSc focused on data Science/computer Science/engineering
        4+ years experience Developing and shipping production grade machine learning systems
        2+ years building and shipping data Science based personalization services and recommendation systems
        experience in data Science or machine learning engineering
        Strong analytical and data Science skills""",
        "Hiring Company" : "XYZ Corporation", 
        "Applicant Name" : "John Smith", 
        "Past Working Experience" : "Data Analyst at ABC Company",
        "Current Working Experience" : "Machine Learning Engineer at DEF Company",
        "Skillsets" : "Python, R, scikit-learn, Keras, Tensorflow",
        "Qualifications" : "BSc in Computer Science, 5+ years of experience in data science and machine learning",
        "EXTRA FIELD" : "",
        "EXTRA SECOND FIELD" : "Data", 
    })
    assert response.status_code == 400
    assert b"Form read error." in response.data  

@responses.activate
def testQueryModel(client): 
    # expected response from LLM model server 
    modelOutput = """Dear Hiring Manager,

        I am writing to express my interest in the Data Scientist position at XYZ Corporation. With over four years of experience developing and shipping production-grade machine learning systems and two years building and shipping data science-based personalization services and recommendation systems, I am confident that my background and skills make me an ideal candidate for this role.

        As a Data Scientist with a strong analytical and data science skillset, I have extensive experience in working with Python, R, scikit-learn, Keras, and TensorFlow. My previous work as a Data Analyst at ABC Company has honed my skills in data visualization and statistical analysis, which I believe would be valuable in a Data Scientist role.

        In addition to my technical expertise, I possess strong communication and collaboration skills, which I bring to the team through my past experience in machine learning engineering and data science projects. My ability to work collaboratively with cross-functional teams is also a significant strength.

        I am excited about the opportunity to join XYZ Corporation, where I can leverage my knowledge of data science and machine learning to contribute to innovative business solutions. I am confident that my skills and experiences align well with the needs of the company and I look forward to discussing how I can contribute to its success.

        Thank you for considering my application. I am looking forward to the opportunity to discuss how I can further contribute to your organization.

        Sincerely,
        John Smith"""

    # mock API response from LLM model server 
    responses.add(
        responses.POST,
        "http://0.0.0.0:8000/query",
        json={"modelOutput": modelOutput},
        status=200
    )

    client.set_cookie(key='access_token_cookie', value=accessTokenCookie)

    response = client.post("model/query", 
        headers= {"X-CSRF-TOKEN": csrfAccessToken},
        data={
        "Job Title" : "Data Scientist", 
        "Preferred Qualifications" : """BSc focused on data Science/computer Science/engineering
        4+ years experience Developing and shipping production grade machine learning systems
        2+ years building and shipping data Science based personalization services and recommendation systems
        experience in data Science or machine learning engineering
        Strong analytical and data Science skills""",
        "Hiring Company" : "XYZ Corporation", 
        "Applicant Name" : "John Smith", 
        "Past Working Experience" : "Data Analyst at ABC Company",
        "Current Working Experience" : "Machine Learning Engineer at DEF Company",
        "Skillsets" : "Python, R, scikit-learn, Keras, Tensorflow",
        "Qualifications" : "BSc in Computer Science, 5+ years of experience in data science and machine learning", 
    })
    assert response.status_code == 201
    assert b"Dear Hiring Manager," in response.data 
    assert b"John Smith" in response.data 