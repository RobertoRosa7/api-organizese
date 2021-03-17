from flask import g

def get(*args, **kwargs):
  return g.get(*args, **kwargs)


def set_user(key, value):
  g.__setattr__(key, value)


def get_user():
  return g.get("user", {})


# def g_get_usuario():
#   return get_user().get("usuario", {})


# def g_get_email():
#   return g_get_usuario().get("email", None)


def get_id():
  return get_user().get("_id")
