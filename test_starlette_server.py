""" imports """
import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# test client and server instance 
from starlette.testclient import TestClient
from model_server.app import app 

""" 
Run test by 'pytest' in powershell. ETA: 250 seconds (due to model inference)

"""

def testValidModelInference():
    """
    GIVEN a starlette application configured for testing
    WHEN a user prompt is posted to '/query'
    THEN check that a '200' status code is returned
    """
    with TestClient(app) as client:
        prompt = "Generate Cover Letter using this information:Job Title:  Data Scientist, Preferred Qualifications: BSc focused on data Science/computer Science/engineering\n4+ years experience Developing and shipping production grade machine learning systems\n2+ years building and shipping data Science based personalization services and recommendation systems\nexperience in data Science or machine learning engineering\nStrong analytical and data Science skills, Hiring Company: XYZ Corporation, Applicant Name: John Smith, Past Working Experience: Data Analyst at ABC Company, Current Working Experience: Machine Learning Engineer at DEF Company, Skillsets:Python, R, scikit-learn, Keras, Tensorflow, Qualifications: BSc in Computer Science, 5+ years of experience in data science and machine learning"
        response = client.post(
            "/query", 
            data=prompt, 
        )
        assert response.status_code == 200

