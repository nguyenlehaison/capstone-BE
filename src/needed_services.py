from flask import jsonify


def server_response(success, message, code):
    return jsonify({
        "success": success,
        "error": code,
        "message": message
    }), code


def server_drink_response(success, drinks, code):
    return jsonify({
        'success': success,
        'drinks': drinks
    }), code


def server_drink_delete_response(success, id, code):
    return jsonify({
        'success': success,
        'delete': id
    }), code
