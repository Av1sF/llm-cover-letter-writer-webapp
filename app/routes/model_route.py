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
from setup.llm_model import model

# initate blueprint  
modelRoute = Blueprint('model', __name__, url_prefix="/model")

@jwt_required()
@modelRoute.route('/query', methods=['POST'])
async def queryModel():
    try:
        if request.method == 'POST':
            formData = request.form.to_dict()
            prompt = model.formatUserData(formData)
            modelOutput = await model.inference(prompt)
            
            return make_response(jsonify({"modelOutput": modelOutput}), 200)
    except:
        pass 