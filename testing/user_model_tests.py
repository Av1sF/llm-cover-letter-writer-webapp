# Import sys module for modifying Python's runtime environment
import sys
# Import os module for interacting with the operating system
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# our db model 
from app.models.user import Users

"""
Tests the interface class of the Users model 
To run: 'pytest testing\user_model_test.py' in powershell 
"""

def testNewUser():
    user = Users(
            username="dbtesting",
            email="dbtesting@gmail.com",
            password="Dm@3Eby/WxHN" # store hashed passwords only
        )
    assert user.username == "dbtesting"
    assert user.email == "dbtesting@gmail.com"
    assert user.password == "Dm@3Eby/WxHN"
