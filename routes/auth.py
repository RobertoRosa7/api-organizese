import os, sys
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth

sys.path.append(os.path.abspath(os.getcwd()))

from utils.gets import set_user, get_user
from utils.LoginManager import LoginManager
from enviroment.enviroment import db

auth = HTTPBasicAuth()

def get_token():
  return request.headers.get('token', None)

@auth.verify_password
def _check_password(username, password):
  login_manager = LoginManager()
  token = get_token().replace('Bearer ','')

  if token:
    user_exists = login_manager.verify_auth_token(token, db.collection_users)
    if user_exists:
      set_user('user', user_exists)

  return True

def login_required(func):
  def __callback__(*args, **kwargs):
    if not get_user():
      return jsonify({"status":401,"message":"Usuário ou senha inválido."}), 401

    return func(*args, **kwargs)
  
  __callback__.__name__ = func.__name__
  return auth.login_required(__callback__)

def check_password(func):
  return auth.verify_password(func)