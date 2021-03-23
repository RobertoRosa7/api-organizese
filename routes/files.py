# -*- coding: utf-8 -*-
import os, sys, magic, time

sys.path.append(os.path.abspath(os.getcwd()))

from flask import Blueprint, jsonify, send_file
from flask.globals import request

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


@files.route("/download", methods=["GET"])
def download():
  try:
    release = request.args.get('release', type=str)
    system_os = request.args.get('system', type=str)

    who_is_downloading = {}
    who_is_downloading['user_agent'] = request.user_agent.string
    who_is_downloading['id_address'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    who_is_downloading['when_downloaded'] = int(time.time())
    who_is_downloading['what_downloaded'] = release

    if not release:
      return jsonify({'message': 'nome da imagem é necessário'}), 404

    file = 'files/downloads/' + system_os +  '/' + release

    if not file:
      return jsonify({'message': 'Release não encontrada'}), 404

    mime = magic.from_file(file, mime=True)
    return send_file(file, mimetype=mime, attachment_filename=release, as_attachment=True)
  except Exception as e:
    return not_found(e)


@files.route("/download_list", methods=["GET"])
def get_download_list():
  try:
    download_list = {}  
    linux_list = os.listdir(os.path.join(os.getcwd() + '/files/downloads/linux/'))
    win_list = os.listdir(os.path.join(os.getcwd() + '/files/downloads/windows/'))
    # mac_list = os.listdir(os.path.join(os.getcwd() + '/files/downloads/mac/'))
    
    props = {}
    arr_linux = []
    arr_win = []
    # arr_mac = []

    for i in linux_list:
      arr_linux.append({
        'version':i.split('_')[1],
        'label': 'Linux - Ubuntu 20.04 LTS',
        'release':i,
        'system':'linux'
      })
    
    for i in win_list:
      arr_win.append({
        'version':i.split('_')[1],
        'label': 'Windows',
        'release':i,
        'system':'windows'
      })

    # for i in mac_list:
    #   arr_mac.append({
    #     'version':i.split('_')[1],
    #     'label': 'Mac OS',
    #     'release':i,
    #     'system':'mac'
    #   })


    download_list['linux'] = arr_linux
    download_list['windows'] = arr_win
    # download_list['mac'] = arr_mac
    
    # pprint.pprint(arr_linux)

    # user['linux'] = os.listdir(os.path.join(os.getcwd() + '/files/downloads/linux/'))
    # user['windows'] = os.listdir(os.path.join(os.getcwd() + '/files/downloads/windows/'))
    # user['mac'] = os.listdir(os.path.join(os.getcwd() + '/files/downloads/mac/'))

    # print(os.listdir(os.path.join(os.getcwd() + '/files/downloads/')))

    return jsonify({'message': 'releases', 'download_list': download_list}), 200
  except Exception as e:
    return not_found(e)


@files.errorhandler(500)
def not_found(e=None):
  return {'message': 'Error %s' % repr(e), 'status': 500}, 500