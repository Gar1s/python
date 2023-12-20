from flask import jsonify, request
from flask_jwt_extended import jwt_required

from application import db
from sqlalchemy.exc import IntegrityError
from . import phone_call_api_bp

from application.phone_call.models import PhoneCall


@phone_call_api_bp.route('/calls', methods=['GET'])
@jwt_required()
def get_phone_calls():
    calls = PhoneCall.query.all()
    
    call_dict = []
    
    for call in calls:
        item = dict(
            id = call.id,
            number_of_caller = call.number_of_caller,
            number_of_receiver = call.number_of_receiver,
            caller = call.caller,
            receiver = call.receiver
        )
        call_dict.append(item)
        
    return jsonify(call_dict)

@phone_call_api_bp.route('/call', methods=['POST'])
@jwt_required()
def post_call():
    new_data = request.get_json()
    
    if not new_data:
        return jsonify(message='no input data provided'), 400
    
    if not new_data.get('number_of_caller') or not new_data.get('number_of_receiver') or not new_data.get('caller') or not new_data.get('receiver'):
        return jsonify(message='incorrect keys'), 422
    
    call = PhoneCall(number_of_caller=new_data.get('number_of_caller'), 
                     number_of_receiver=new_data.get('number_of_receiver'),
                     caller=new_data.get('caller'),
                     receiver=new_data.get('receiver'))
    db.session.add(call)
    db.session.commit()
    
    new_call = PhoneCall.query.filter_by(id=call.id).first()
    
    return jsonify({
        "id": new_call.id,
        "number_of_caller": new_call.number_of_caller,
        "number_of_receiver": new_call.number_of_receiver,
        "caller": new_call.caller,
        "receiver": new_call.receiver
    }), 201