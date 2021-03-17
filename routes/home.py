# -*- coding: utf-8 -*-
import os, sys, json

sys.path.append(os.path.abspath(os.getcwd()))

from flask import Blueprint, jsonify

home = Blueprint("home", __name__, url_prefix="/home")


@home.route("/", methods=["GET"])
def health():
    try:
      lista_ativos = [
        {
          '$project': {
            '_id': 0, 
            'codigo_ativo': 1, 
            'nome_empresa': '$dados_companhia.denom_social'
            }
          }, 
        {
          '$sort': {
            'codigo_ativo': 1
            }
        }
      ]
      return jsonify(lista_ativos=lista_ativos)
    except Exception as e:
      return jsonify(error=e)

    