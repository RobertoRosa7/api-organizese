from flask import request
import base64
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from utils.gets import g
from utils.Cipher import CipherPoet

class TokenManager:
  ...
    # def __init__(self, key='Y308A10EQVQOFMBIXFMYZZCSGV6CUF8M'):
    #     self._key = key

    # @classmethod
    # def mount(cls, key):
    #     return TokenManager(key=key)

    # @staticmethod
    # def __encrypt_data(data):
    #     for key in data:
    #         value = str(data[key])
    #         data[key] = base64.encodebytes(CipherPoet.encrypt(value)).decode()
    #     return data

    # @staticmethod
    # def __decrypt_data(data):
    #     for key in data:
    #         value = base64.decodebytes(data[key].encode())
    #         data[key] = CipherPoet.decrypt(value).decode()
    #     return data

    # @staticmethod
    # def generate_token(private_key, data, expiration=2628000000):
    #     return Serializer(private_key, expires_in=expiration).dumps(data)

    # @staticmethod
    # def verify_token(private_key, token):
    #     data = None
    #     try:
    #         data = Serializer(private_key).loads(token)
    #     except SignatureExpired:
    #         print('Token expirado')
    #         pass
    #     except BadSignature:
    #         print('Token Invalido')
    #         pass
    #     return data

    # def generate_auth_token(self, data, encrypt_data=False):
    #     if encrypt_data:
    #         data = self.__encrypt_data(data)
    #     return self.generate_token(self._key, data).decode()

    # def verify_auth_token(self, token, encrypt_data=False):
    #     if token is None:
    #         return None
    #     elif isinstance(token, str):
    #         token = token.encode()
    #     data = self.verify_token(self._key, token)
    #     if data is None:
    #         return None
    #     elif encrypt_data:
    #         data = self.__decrypt_data(data)
    #     return data


class LoginRequired:
    ...
    # def __init__(self, token_name, encrypt_payload=False, token_manager=None, g_variable=None):
    #   self.token_manager = token_manager
    #   if self.token_manager is None:
    #       self.token_manager = TokenManager()
    #   self.token_name = token_name
    #   self.encrypt_payload = encrypt_payload
    #   self.g_variable = g_variable
    #   self.func = None

    # def __call__(self, func):
    #   def __callback__(*args, **kwargs):
    #     token = request.headers.get(self.token_name)
    #     data = self.token_manager.verify_auth_token(token, self.encrypt_payload)
    #     if not data:
    #         return "{'status':401,'message':'Usuário ou senha inválido.'}", 401
    #     if self.g_variable:
    #         g.set(self.g_variable, data)
    #         return self.func(*args, **kwargs)
    #     return self.func(data, *args, **kwargs)
    #   self.func = func
    #   if hasattr(func, "__name__"):
    #       name = func.__name__
    #   else:
    #       name = "__func__" + str(id(func))
    #   __callback__.__name__ = name
    #   return __callback__

login_required = LoginRequired
