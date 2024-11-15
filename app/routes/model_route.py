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

client = httpx.Client()
client = httpx.Client(timeout=None)

@jwt_required()
@modelRoute.route('/query', methods=['POST'])
async def queryModel():
    try:
        if request.method == 'POST':
            formData = request.form.to_dict()

            # gets text/plain type response 
            prompt = formatPrompt(formData)
            response = client.post("http://localhost:8000/query",
                data=prompt,
            )
            return make_response(response.json(), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"modelOutput":"unable to generate output."}), 500)