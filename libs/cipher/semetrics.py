
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import hashlib


class Cipher():
    def __init__(self, instance) -> None:
        self.instance = instance
        self.private_key = RSA.importKey(self.instance.payer.private_key)
        self.public_key = RSA.importKey(self.instance.payer.public_key)

    def verify_signature(self, data)-> bool:
        hasher = hashlib.sha256()
        hasher.update(bytes(data, encoding='utf8'))
        data_h = hasher.hexdigest()

        enc = binascii.unhexlify(self.instance.signature)
        dec_txt = self.decrypt(enc)


        # print(dec_txt)
        if data_h == dec_txt.decode("utf-8") :
            return True
        return False
        ...

    def decrypt(self, exText):
        decryptor = PKCS1_OAEP.new(self.private_key)
        decrypted = decryptor.decrypt(exText)
        return decrypted

    def encrypt(self, in_use=False):
        hasher = hashlib.sha256()
        hasher.update(bytes(self.instance.data, encoding='utf8'))
        data = hasher.hexdigest()

        print(data)
        
        encryptor = PKCS1_OAEP.new(self.public_key)
        encrypted = encryptor.encrypt(bytes(str(data), encoding='utf8'))
        if in_use:
            return encrypted
        else:
            return binascii.hexlify(encrypted).decode("utf-8") 
        
