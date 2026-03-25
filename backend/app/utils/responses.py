from flask import jsonify


def success_response(data: dict | None = None, status: int = 200):
    return jsonify(data or {}), status


def error_response(code: str, message: str, details: dict | None = None, status: int = 400):
    return jsonify({
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        }
    }), status
