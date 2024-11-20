""" imports """
from flask import (Blueprint, 
        request, 
        jsonify,  
        make_response)
from models.user import Users
from database.db import db 
from flask_jwt_extended import (
    jwt_required
)
from setup.llm_format import (
    formatPrompt,
    PROMPTKEYS,
    )
import requests

# initate blueprint  
modelRoute = Blueprint('model', __name__, url_prefix="/model")

@modelRoute.route('/query', methods=['POST'])
@jwt_required()
async def queryModel():
    try:
        # turn json to dictionary 
        formData = request.form.to_dict()
        assert (sorted(list(formData.keys()))) == sorted(PROMPTKEYS)
        # format dictionary information to create user prompt for model 
        prompt = formatPrompt(formData)
    except Exception as e:
        print(e)
        return make_response(jsonify({"modelOutput":"Form read error."}), 400)

    try:
        # query model by sending request to model server 
        response = requests.post("http://localhost:8000/query",
            data=prompt,
        )
        # send back model response to user 
        return make_response(response.json(), 201)
    except Exception as e:
        return make_response(jsonify({"modelOutput":"unable to generate output."}), 500)