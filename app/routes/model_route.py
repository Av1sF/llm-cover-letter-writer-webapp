""" imports """
from flask import (Blueprint, 
        request, 
        jsonify,  
        make_response)
from app.models.user import Users
from app.database.db import db 
from flask_jwt_extended import (
    jwt_required
)
from app.setup.llm_format import formatPrompt
import httpx 

# initate blueprint  
modelRoute = Blueprint('model', __name__, url_prefix="/model")

# initalise httpx  
client = httpx.Client()
# disable timeout due to long inference times 
client = httpx.Client(timeout=None)

@jwt_required()
@modelRoute.route('/query', methods=['POST'])
async def queryModel():
    try:
        if request.method == 'POST':
            # turn json to dictionary 
            formData = request.form.to_dict()
            # format dictionary information to create user prompt for model 
            prompt = formatPrompt(formData)
            # query model by sending request to model server 
            response = client.post("http://localhost:8000/query",
                data=prompt,
            )
            # send back model response to user 
            return make_response(response.json(), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"modelOutput":"unable to generate output."}), 500)