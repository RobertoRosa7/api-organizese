# -*- coding: utf-8 -*-
import os, sys, re, base64

from flask.globals import request

sys.path.append(os.path.abspath(os.getcwd()))

from flask import Blueprint, jsonify, render_template, make_response
from routes.auth import login_required
from utils.login_manager import LoginManager
from enviroment.enviroment import db, API
from utils.send_email import send_verify_email
from utils.gets import set_user, get_user
from bson.json_util import ObjectId

my_login = Blueprint("my_login", __name__, url_prefix="/login")


def valida_sufixos_hosts_email(email):
  suffixes = ['con', 'com.bt', 'combr', 'xom', 'vom', 'ckm', 'c', 'clm']
  hosts = ['gmai', 'yaho', 'outlok', 'gnail', 'hotmai', 'gmaol', 'gemail', 'outloo', 'ganil', 'gamil', 'hotnail', 'g.mail', 'gmnail', 'hotmaim', 'hotmais', 'hotmaiil', 'msm']
  splitAddress = email.split('@')
  splitAddress = splitAddress[1].split('.')
  
  if splitAddress[0] in hosts:
    return False
  else:
    addr = ('.').join(splitAddress[1:])
    if addr in suffixes:
      return False
  return True


@my_login.route('/signin', methods=['GET'])
def sign_in():
  access = request.headers.get('Authorization')

  if not access:
    return jsonify({"message": 'e-mail e senha é obrigatório'}), 401
  
  access = access.split(':')
  access_email = base64.b64decode(access[0])
  access_pass = base64.b64decode(access[1])
  
  if not access_email or not access_pass:
    return jsonify({"message": 'Campo e-mail é obrigatório'}), 404
  
  try:
    login_manager = LoginManager()
    user = db.collection_users.find_one({'email': access_email.decode('ascii')})
    
    if not user:
      return jsonify({"message": 'E-mail não cadastrado'}), 404
    
    check_pass = login_manager.check_password(access_pass.decode('ascii'), user['password'])

    if not check_pass:
      return jsonify({"message": 'E-mail ou senha inválidos'}), 401

    if not user['verified']:
      return jsonify({"message": 'E-mail não foi verificado'}), 401

    if isinstance(user['_id'], ObjectId):
      user['_id'] = str(user['_id'])

    token = login_manager.generate_auth_token(user)
    set_user('user', user)
  
    return {'access_token': token.decode('ascii')}, 200
  except Exception as e:
    return not_found(e)


@my_login.route('/signup', methods=['POST'])
def create_user():
  data = request.get_json()
  login_manager = LoginManager()

  if 'email' not in data:
      return jsonify({"message": 'Campo e-mail é obrigatório'}), 401
  
  regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
  match = re.match(regex, data['email'].lower())

  if match is None or not valida_sufixos_hosts_email(data['email']):
      return jsonify({"message": 'Campo e-mail inválido'}), 401

  user = {**data, 'email': data['email'],'password': login_manager.password_to_hash(data['password'])}
  
  try:
    user_exists = db.collection_users.find_one({'email': user['email']})
    there_is_user = user_exists if user_exists else {}

    if 'password' in there_is_user:
      return jsonify({'message': 'Usuário já cadastro'}), 400
      
    user['_id'] = db.collection_users.insert_one(user).inserted_id
    user['_id'] = str(user['_id'])
    token = login_manager.generate_auth_token(user, 600000).decode('ascii')
    template = render_template('bem-vindo.html', token=token, api_url=API)
    is_sended = send_verify_email(template, user['email'])

    if not is_sended['status']:
      return jsonify({'message': 'Não foi possível enviar email de validação'}), 400

    return jsonify({"message": 'Usuário cadastrado com sucesso'}), 201
  except Exception as e:
    return not_found(e)


@my_login.route('/reset_password', methods=['GET'])
def reset_password():
  try:
    login_manager = LoginManager()
    access = request.headers.get('Authorization')

    if not access:
      return jsonify({"message": 'senha é obrigatório'}), 401

    access = access.split(':access:')
    password = base64.b64decode(access[0]).decode('ascii')
    token = access[1]
    
    if not token or not password:
      return jsonify({"message": 'senha e token são obrigatórios'}), 401
    
    user_verified = login_manager.verify_auth_token(token, db.collection_users)
    
    if not user_verified:
      return jsonify({'message': 'token inválido'}), 401

    email = user_verified['email']
    new_password = login_manager.password_to_hash(password)
    user_exists = db.collection_users.find_one({'email': email})

    if not user_exists:
      return jsonify({'message': 'Usuário não cadastrado'}), 404
    
    is_update = db.collection_users.update({'email': email}, {'$set': {'password': new_password}})

    if is_update['nModified'] > 0:
      return {'message': 'Senha atualizada com sucesso'}, 200
    else:
      return {'message': 'A nova senha deve ser diferente da antiga'}, 401
  except Exception as e:
    return not_found(e)


@my_login.route('/login_verified', methods=['POST'])
def login_verified():
  payload = request.get_json()
  login_manager = LoginManager()

  if not payload['token']:
    return jsonify({'message': 'Nenhum token recebido!'}), 400

  token = payload['token']
  token_verified = login_manager.verify_auth_token(token, db.collection_users, purge_private=True)
  
  if not token_verified:
    return jsonify({'message', 'token inválido ou experiado'}), 400

  db.collection_users.update({'email': token_verified['email']}, {'$set': {'verified': True}})

  return {'message': 'E-mail verificado!'}, 200


@my_login.route('/email_to_reset', methods=['POST'])
def email_to_reset():
  payload = request.get_json()
  login_manager = LoginManager()

  if 'email' not in payload:
    return jsonify({'message', 'E-mail é obrigatório'}), 401
  
  user_exists = db.collection_users.find_one({'email': payload['email']})

  if not user_exists:
    return jsonify({'message': 'E-mail não encontrado'}), 404
  
  user_exists['_id'] = str(user_exists['_id'])
  token = login_manager.generate_auth_token(user_exists, 600000).decode('ascii')
  template = render_template('reset_password.html', email=user_exists['email'], token=token, api_url=API)
  
  try:
    send_verify_email(template, user_exists['email'])
    return {'message': 'Email de recuperação de senha enviado.'}, 200
  except Exception as e:
    return not_found(e)


@my_login.errorhandler(500)
def not_found(e=None):
  return {'message': 'Error %s' % repr(e), 'status': 500}, 500