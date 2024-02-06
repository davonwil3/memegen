from flask import request, jsonify
from functools import wraps
import firebase_admin
from firebase_admin import auth
import logging

def verify_firebase_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header is missing or not valid."}), 401

        id_token = auth_header.split('Bearer ')[1]

        try:
            auth.verify_id_token(id_token)
        except Exception as e:
            logging.error(f"Firebase token verification failed: {e}")
            return jsonify({"error": "Invalid or expired Firebase ID token.", "details": str(e)}), 403

        return f(*args, **kwargs)
    return decorated_function


