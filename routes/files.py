# -*- coding: utf-8 -*-
import os, sys, pprint, time

sys.path.append(os.path.abspath(os.getcwd()))

from flask import Blueprint, jsonify, send_file
from flask.globals import request
from routes.auth import login_required
from enviroment.enviroment import db
from utils.gets import get_user
from utils.login_manager import LoginManager

files = Blueprint("files", __name__, url_prefix="/files")

@files.route("/images", methods=["GET"])
def get_images():
  try:
    name_image = request.args.get('name', type=str)
    if not name_image:
      return jsonify({'message': 'nome da imagem é necessário'}), 404
    file = 'files/images/' + name_image + '.svg'
    return send_file(file, mimetype='image/svg+xml', attachment_filename=name_image + '.svg')
  except Exception as e:
    return not_found(e)


@files.route("/download_list", methods=["GET"])
def get_download_list():
  try:
    download_list = {}
    download_list['user_agent'] = request.user_agent.string
    # download_list['origin'] = request.headers['Origin']
    download_list['id_address'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    download_list['first_access'] = int(time.time())

    linux_list = os.listdir(os.path.join(os.getcwd() + '/files/downloads/linux/'))
    win_list = os.listdir(os.path.join(os.getcwd() + '/files/downloads/windows/'))
    mac_list = os.listdir(os.path.join(os.getcwd() + '/files/downloads/mac/'))

    props = {}
    arr_linux = []
    arr_win = []
    arr_mac = []

    for i in linux_list:
      props['version'] = i.split('_')[1]
      props['label'] = 'Linux - Ubuntu 20.04 LTS'
      props['release'] = i
      arr_linux.append(props)

    for i in win_list:
      props['version'] = i.split('_')[1]
      props['label'] = 'Windows'
      props['release'] = i
      arr_win.append(props)

    for i in mac_list:
      props['version'] = i.split('_')[1]
      props['label'] = 'Mac OS'
      props['release'] = i
      arr_mac.append(props)


    download_list['linux'] = arr_linux
    download_list['windows'] = arr_win
    download_list['mac'] = arr_mac

    # user['linux'] = os.listdir(os.path.join(os.getcwd() + '/files/downloads/linux/'))
    # user['windows'] = os.listdir(os.path.join(os.getcwd() + '/files/downloads/windows/'))
    # user['mac'] = os.listdir(os.path.join(os.getcwd() + '/files/downloads/mac/'))

    # print(os.listdir(os.path.join(os.getcwd() + '/files/downloads/')))

    return jsonify({'message': 'releases', 'donwload_list': download_list}), 200
  except Exception as e:
    return not_found(e)

@files.errorhandler(500)
def not_found(e=None):
  return {'message': 'Error %s' % repr(e), 'status': 500}, 500