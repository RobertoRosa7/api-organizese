import rsa

# -----BEGIN RSA PRIVATE KEY-----
# MIICXQIBAAKBgQDDOqcWZe2RFQAEQAC7hr0WbwkYJEFDVEW05sbsgg2oy5GFwgwavsej7kpJbo9OliKVT5N3euTH/hljPERLKQ3ObLUuzcFCdKwjt8GEuw67FkCKNqvnh56S2trtHlPWqTXYfu1lWUEehIMUHofoPIDsazI5PY+cmxpwynJzCZzkqwIDAQABAoGBAKDa/Ly5suotMVxPF8trEvUe+5FGnfdJwj1xQEmyRmrjf72DytFmi7uIJPEoBS+tCEWZ0VlKiqI1vNlE2MhMxS/1OfRRwmC8PjZjii9EBrK+IvD/zph8gxXHS1Eqmh/ndiUsi3oVl+iPPbv5vbzv8iHViXEThTaJQZXKM/iffdDRAkEA6Et1f11R62OQRUIGMR3CdzLLCfy7QYfkhG41/8Io5AU/DkPQonLWT+e7MrBSu66fLzEKf/nx/dCT2L/7+p7GvwJBANcm4QvCHF4qRN9bMasqckdbk+fIHkX6EqwsVNwMQe0F1VL2VVeISVQQ723KwHnzmloJee1LvIEgfSZyGTW+KRUCQQDb2odTSzR8T5g9JHcNx3fFLyqhwjRMmlw6xsCO1umynhCG5MIy7fNOXyl6mQ1EmsoIdSbV5u8U5XL4wwOuuNWrAkAMEI8QFLt4gFBKYhe/7GpqG/WISs1/yQ0hAH9ls35C50/WDiAs/2R1RVnXw0XV0NY39E4VA2k3qHW8ISvOurIdAkAnn/g+rRHIxOtvzbLYfxGunxo5yRXKc5bTaQOBd42Rl1m4oaBLyW/iA7Pg+49kErw9+3KPGCLFtttOdprxrqYk
# -----END RSA PRIVATE KEY-----
#
# -----BEGIN PUBLIC KEY-----
# MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDOqcWZe2RFQAEQAC7hr0WbwkY
# JEFDVEW05sbsgg2oy5GFwgwavsej7kpJbo9OliKVT5N3euTH/hljPERLKQ3ObLUu
# zcFCdKwjt8GEuw67FkCKNqvnh56S2trtHlPWqTXYfu1lWUEehIMUHofoPIDsazI5
# PY+cmxpwynJzCZzkqwIDAQAB
# -----END PUBLIC KEY-----


def obfuscate_str(_str, power=0.7):
    _str = str(_str)
    if not _str or not power:
        return _str
    power = -power if power < 0 else power
    power = 1.0 if power > 1.0 else power
    _l = len(_str)
    _p = int(_l * power)
    _b = _l - _p
    if _b < 2:
        return _str[:_b] + "*" * _p
    _b = int(_b/2)
    _p = _l - _b - ((_b % 2) + _b)
    return _str[:_b] + "*" * _p + _str[_b+_p:]


class CipherPoet:
    @classmethod
    def get_new_keys_pair(cls):
        return rsa.newkeys(1024)

    @classmethod
    def mount_public_key(cls, key_str):
        return rsa.PublicKey.load_pkcs1_openssl_pem(key_str)

    @classmethod
    def get_default_public_key_str(cls):
        return b"-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDOqcWZe2RFQAEQAC7hr0WbwkYJEFDVEW05sbsgg2oy5GFwgwavsej7kpJbo9OliKVT5N3euTH/hljPERLKQ3ObLUuzcFCdKwjt8GEuw67FkCKNqvnh56S2trtHlPWqTXYfu1lWUEehIMUHofoPIDsazI5PY+cmxpwynJzCZzkqwIDAQAB\n-----END PUBLIC KEY-----"

    @classmethod
    def get_default_public_key(cls):
        strp = cls.get_default_public_key_str()
        return cls.mount_public_key(strp)

    @classmethod
    def get_default_private_key_str(cls):
        return b"-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQDDOqcWZe2RFQAEQAC7hr0WbwkYJEFDVEW05sbsgg2oy5GFwgwavsej7kpJbo9OliKVT5N3euTH/hljPERLKQ3ObLUuzcFCdKwjt8GEuw67FkCKNqvnh56S2trtHlPWqTXYfu1lWUEehIMUHofoPIDsazI5PY+cmxpwynJzCZzkqwIDAQABAoGBAKDa/Ly5suotMVxPF8trEvUe+5FGnfdJwj1xQEmyRmrjf72DytFmi7uIJPEoBS+tCEWZ0VlKiqI1vNlE2MhMxS/1OfRRwmC8PjZjii9EBrK+IvD/zph8gxXHS1Eqmh/ndiUsi3oVl+iPPbv5vbzv8iHViXEThTaJQZXKM/iffdDRAkEA6Et1f11R62OQRUIGMR3CdzLLCfy7QYfkhG41/8Io5AU/DkPQonLWT+e7MrBSu66fLzEKf/nx/dCT2L/7+p7GvwJBANcm4QvCHF4qRN9bMasqckdbk+fIHkX6EqwsVNwMQe0F1VL2VVeISVQQ723KwHnzmloJee1LvIEgfSZyGTW+KRUCQQDb2odTSzR8T5g9JHcNx3fFLyqhwjRMmlw6xsCO1umynhCG5MIy7fNOXyl6mQ1EmsoIdSbV5u8U5XL4wwOuuNWrAkAMEI8QFLt4gFBKYhe/7GpqG/WISs1/yQ0hAH9ls35C50/WDiAs/2R1RVnXw0XV0NY39E4VA2k3qHW8ISvOurIdAkAnn/g+rRHIxOtvzbLYfxGunxo5yRXKc5bTaQOBd42Rl1m4oaBLyW/iA7Pg+49kErw9+3KPGCLFtttOdprxrqYk\n-----END RSA PRIVATE KEY-----"

    @classmethod
    def mount_private_key(cls, key_str):
        return rsa.PrivateKey._load_pkcs1_pem(key_str)

    @classmethod
    def get_default_private_key(cls):
        strp = cls.get_default_private_key_str()
        return cls.mount_private_key(strp)

    @classmethod
    def get_default_key_pair(cls):
        return cls.get_default_public_key(), cls.get_default_private_key()

    @classmethod
    def prepare_message(cls, message):
        b = str.encode(message)
        return b

    @classmethod
    def encrypt(cls, plaintext, public_key=None, prepare_message=True) -> bytes:
        if not public_key:
            public_key = cls.get_default_public_key()
        if prepare_message:
            plaintext = cls.prepare_message(plaintext)
        return rsa.encrypt(plaintext, public_key)

    @classmethod
    def decrypt(cls, cipher, private_key=None) -> bytes:
        if not private_key:
            private_key = cls.get_default_private_key()
        return rsa.decrypt(cipher, private_key)

    @classmethod
    def parse_public_key_to_dict(cls, key):
        return {"n": key.n, "e": key.e}

    @classmethod
    def parse_private_key_to_dict(cls, key):
        return {"n": key.n, "e": key.e, "d": key.d, "p": key.p, "q": key.q}


class StorageCipher:
    _pri_key_str = b"-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCAnYyR3ez4CcYW5oaRipdMTWkNCOecYe8Jn0gBMsKZzN/rRvf4pf7484GvGuxGSwHY2qrBh3ni9abYAHsMKp7IGGiwFyF+WM3DwGc8e+io2qbCvLWqalTVSY3QldCI4b7H5eFzrFO8xhzFNcdv3tHthwU/k2nuHJmfsvfD0SoKlwIDAQABAoGARukWSJIIBdU1rwiYZwP3WO1RHwuqzvC73x0/kNGQs0Veq5RsQV4cDtwKwyVf4X2XXh1pidwM2pI/09WoAdQ5yCYrpwz1/p7KR3JuZRsUQnuQqcfpdHNXxzqy75T02tJ7vRfZuZCOCwaKCkfGAsk49Aqh1d7tEDKrhmJxxqC73SkCQQDAE3l4/f8M4EJWDNuFqwxRm2jKDAG3Rs+TDmdaZMw/p8bS5tFvXyIM+VX/M+WBkjfprgUDi5k0CLIbnubexMS7AkEAq2tYWhLHnwN1xuXJBaXXUC365j+NarHX3rXrqqMX0FuL/5wwSDHpzucixJ7CUcXq4dFI0138t5GUW00YL/7h1QJBAJ4kqqQCxKcOUa/VwDyK+4aJZTrNre//nlJezpuvWDek5N+qaY/ADSIPfE21peYLxHti6v/jRU2BR1vUdhO+gJcCQFjMIZd/VPMVWsRusiR/1TqOpwLw9vPHLpkKygq5s5NWaP4/TW+Ik6J/by5FQ0oS6WqS/FOpw0jgW+az2Ay8zwUCQB+kY5Zfxc8eu5686XLFYq4ojqGrE7eW8ssboV14OtcJxxiABa//HpZzmA4jxsADOg4gvL13Msz6+1qMjyN9Pzo=\n-----END RSA PRIVATE KEY-----"
    _pub_key_str = b"-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCAnYyR3ez4CcYW5oaRipdMTWkNCOecYe8Jn0gBMsKZzN/rRvf4pf7484GvGuxGSwHY2qrBh3ni9abYAHsMKp7IGGiwFyF+WM3DwGc8e+io2qbCvLWqalTVSY3QldCI4b7H5eFzrFO8xhzFNcdv3tHthwU/k2nuHJmfsvfD0SoKlwIDAQAB\n-----END PUBLIC KEY-----"

    _pri_key = CipherPoet.mount_private_key(_pri_key_str)
    _pub_key = CipherPoet.mount_public_key(_pub_key_str)

    @classmethod
    def encrypt(cls, plaintext, prepare_message=True):
        return CipherPoet.encrypt(plaintext, public_key=cls._pub_key, prepare_message=True)

    @classmethod
    def decrypt(cls, cipher):
        return CipherPoet.decrypt(cipher, private_key=cls._pri_key)