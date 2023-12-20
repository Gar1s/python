from application import db

class PhoneCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_caller = db.Column(db.String(20))
    number_of_receiver = db.Column(db.String(20))
    caller = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)