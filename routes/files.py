# -*- coding: utf-8 -*-
import os, sys, pprint

sys.path.append(os.path.abspath(os.getcwd()))

from flask import Blueprint, jsonify, send_file
from flask.globals import request
from routes.auth import login_required
from enviroment.enviroment import db
from utils.gets import get_user
from utils.login_manager import LoginManager

files = Blueprint("files", __name__, url_prefix="/files")

@files.route("/images", methods=["GET"])
def get_profile():
  try:
    name_image = request.args.get('name', type=str)
    
    print(name_image)

    if not name_image:
      return jsonify({'message': 'nome da imagem é necessário'}), 404
    
    file = 'files/images/' + name_image + '.svg'
    return send_file(file, mimetype='image/svg+xml', attachment_filename=name_image + '.svg')
  except Exception as e:
    return not_found(e)


@files.errorhandler(500)
def not_found(e=None):
  return {'message': 'Error %s' % repr(e), 'status': 500}, 500