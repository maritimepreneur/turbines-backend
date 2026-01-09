from flask import Blueprint, jsonify

user_bp = Blueprint('users', __name__)

@user_bp.route('/users')
def get_users():
    users = [
        {
            'id': 1,
            'name': 'Budi Santoso',
            'email': 'budi@example.com',
            'role': 'admin'
        },
        {
            'id': 2,
            'name': 'Siti Aminah',
            'email': 'siti@example.com',
            'role': 'user'
        },
        {
            'id': 3,
            'name': 'Ahmad Wijaya',
            'email': 'ahmad@example.com',
            'role': 'user'
        }
    ]
    
    return jsonify({
        'status': 'success',
        'total': len(users),
        'data': users
    })