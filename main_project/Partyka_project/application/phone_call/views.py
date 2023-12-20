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

@phone_call_api_bp.route('/call/<int:id>', methods=['GET'])
@jwt_required()
def get_call(id):
    call = PhoneCall.query.filter_by(id=id).first()
    if not call:
        return jsonify(message=f"call with id {id} not found"), 404
    return jsonify({
        "id": call.id,
        "number_of_caller": call.number_of_caller,
        "number_of_receiver": call.number_of_receiver,
        "caller": call.caller,
        "receiver": call.receiver
    }), 200

@phone_call_api_bp.route('/call/<int:id>', methods=['PUT'])
@jwt_required()
def update_call(id):
    call = PhoneCall.query.filter_by(id=id).first()
    if not call:
        return jsonify(message=f"call with id {id} not found"), 404
    new_data = request.get_json()
    if not new_data:
        return jsonify(message='no input data provided'), 400
    if new_data.get('number_of_caller'):
        call.number_of_caller = new_data.get('number_of_caller')
    if new_data.get('number_of_receiver'):
        call.number_of_receiver = new_data.get('number_of_receiver')
    if new_data.get('caller'):
        call.caller = new_data.get('caller')
    if new_data.get('receiver'):
        call.receiver = new_data.get('receiver')
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return jsonify(message='call was updated'), 200

@phone_call_api_bp.route('/call/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_call(id):
      call = PhoneCall.query.get(id)
      db.session.delete(call)
      db.session.commit()
      return jsonify({'message' : 'call has been deleted!'}), 200