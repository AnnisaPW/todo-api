from flask import jsonify
from typing import Any


class ResponseCode:

    @classmethod
    def success_response(cls, code: int, status: str, data=None):
        if data == None:
            response = {"code": code, "status": status}
        else:
            response = {"code": code, "status": status, "data": data}
        return jsonify(response), code

    @classmethod
    def error_response(cls, code: int, status: str):
        response = {"code": code, "status": status}
        return response

    @classmethod
    def server_error_response(cls):
        code = 500
        response = cls.error_response(code, "INTERNAL SERVER ERROR")
        return jsonify(response), code

    @classmethod
    def not_found_response(cls):
        code = 404
        response = cls.error_response(code, "NOT FOUND")
        return jsonify(response), code

    @classmethod
    def bad_request_response(cls, error_msg: Any):
        code = 400
        response = cls.error_response(code, f"{error_msg}")
        return jsonify(response), code
