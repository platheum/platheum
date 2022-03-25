import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
from Crypto.Cipher import PKCS1_OAEP
import binascii


key = RSA.generate(2048)



private_key = key.export_key().decode("utf-8") 
public_key1 = key.publickey().exportKey().decode("utf-8")







class CryptoGraphy():
    def __init__(self, model) -> None:
        ...

    def decrypt(self, exText):
        key1 = RSA.importKey(private_key)
        decryptor = PKCS1_OAEP.new(key1)
        decrypted = decryptor.decrypt(exText)
        return decrypted

    def encrypt(self, data: str=''):
        key = RSA.importKey(public_key1)

        encryptor = PKCS1_OAEP.new(key)
        encrypted = encryptor.encrypt(bytes(data, encoding='utf8'))
        return encrypted


crypto = CryptoGraphy(model=None)
l = crypto.encrypt('salim suleiman')

