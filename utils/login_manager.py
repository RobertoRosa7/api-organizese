from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from bson.objectid import ObjectId


class TokenManager:
  @staticmethod
  def generate_token(private_key, data, expiration=2628000000):
    return Serializer(private_key, expires_in=expiration).dumps(data)

  @staticmethod
  def verify_token(private_key, token):
    data = None
    try:
      data = Serializer(private_key).loads(token)
    except SignatureExpired:
      print('Token expirado')
      pass
    except BadSignature:
      print('Token Invalido')
      pass
    return data


class LoginManager(TokenManager):
  # chave usada para geraçao de tokens
  SECRET_KEY = 'Y308A10EQVQOFMBIXFMYZZCSGV6CUF8M'
  SECRET_KEY_ASSESSOR = 'Z208A10FQVQOFMBIXFMYZZCSGV6CUF8M'

  @classmethod
  def _purge_private_data(cls, user: dict):
    if "password" in user:
      del user["password"]
    return user

  # Codifica a senha para ser gravada no banco de dados
  def password_to_hash(self, password):
    return pwd_context.encrypt(password)
  
  # Decodifica a senha do usuario e compara com a senha do banco de dados
  def check_password(self, password, dbpassword):
    return pwd_context.verify(password, dbpassword)

  # Gera um token utilizando a biblioteca itsdangerous baseado na chave secreta.
  def generate_auth_token(self, user_var, expiration=2628000000):
    return self.generate_token(self.SECRET_KEY, {'_id': user_var['_id']}, expiration=expiration)

  # def generate_auth_token_for_assessor_chat(self, user_var, expiration=2628000000):
  #  return self.generate_token(self.SECRET_KEY_ASSESSOR, {'_id': user_var['_id']}, expiration=expiration)

  def get_objectid_from_token(self, token):
      data = self.verify_token(self.SECRET_KEY, token)
      if not data:
          return False
      return data['_id']

  def verify_auth_token(self, token, collection, purge_private=False):
    if not token:
      return False
    data = self.verify_token(self.SECRET_KEY, token)
    if not data:
      return False

    try:
      user = collection.find_one({'_id': ObjectId(data['_id'])})
    except:
     return False

    user['_id'] = str(user['_id'])
    return user if not purge_private else self._purge_private_data(user)

  # def verify_auth_token_for_assessor(self, token, collection):
  #   data = self.verify_token(self.SECRET_KEY_ASSESSOR, token)
  #   _id = data['_id']

  #   user = collection.find_one({'_id': ObjectId(_id)})
  #   user['_id'] = str(user['_id'])
  #   return user
