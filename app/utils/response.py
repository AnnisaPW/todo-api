from flask import Response, jsonify


def success_response(code: int, status: str, data = None):
  if data==None:
    response = {"code": code, "status": status}
  else:
    response = {"code": code, "status": status, "data":data}
  return jsonify(response), code

def error_response(code: int, status:str):
  response = {"code": code, "status": status}
  return response

def server_error_response():
  code = 500
  response = error_response(code, "INTERNAL SERVER ERROR")
  return jsonify(response), code

def not_found_response():
  code = 404
  response = error_response(code, "NOT FOUND")
  return jsonify(response), code

def bad_request_response(error_msg: any):
  code = 400
  response = error_response(code, f"{error_msg}")
  return jsonify(response), code