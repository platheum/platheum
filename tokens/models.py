from django.db import models
from rest_framework.authtoken.models import Token as T
import jwt
import hashlib
import crypt
from wallets.models import Wallet

class Token(T):
    token_hash = models.CharField(max_length=500, help_text = "The hash key of the refresh token, to help stop premaid refresh token")
    token_salt = models.CharField(max_length=500, help_text = "The token hash salt to secure cracking")
    refresh_token = models.CharField(max_length=500, help_text = "Refresh Token for authorization")

    def get_user_rt(self):
        """create a user signature object for jwt"""
        instance_obj = {
            
        "user": {
            'hash': self.user.hash,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'country': self.user.country,
        }, 
        
            "keyHash": self.token_hash
        }
        return jwt.encode(instance_obj, "secret", algorithm="HS256")

    def generate_rf(self):
        hasher = hashlib.sha256()

        # hash the token-key
        key = bytes(self.key, encoding='utf8')
        hasher.update(key)
        key_hash =  hasher.hexdigest()

        # get salt
        token_salt = crypt.mksalt(crypt.METHOD_SHA512)

        # check salt if unique
        while Token.objects.filter(token_salt=token_salt).first() is not None:
            token_salt = crypt.mksalt(crypt.METHOD_SHA512)


        # join "hashed token-key" with "salt" and encode them
        enc_raw_token_hash = bytes(f'{token_salt}{key_hash}', encoding='utf8')

        # hash them
        hasher.update(enc_raw_token_hash)
        token_hash = hasher.hexdigest()

        self.token_hash = token_hash
        self.save()
        
        # create a jwt object for refresh_token
        return {'new_rt': self.get_user_rt(), 'token_salt': token_salt, 'token_hash': token_hash}

        

    def refresh_t(self):
        """Replace old refresh-token to new one and new token salt"""

        obj = self.generate_rf()

        while Token.objects.filter(refresh_token=obj['new_rt']).first() is not None:
            obj = self.generate_rf()

        self.token_salt = obj['token_salt']
        self.token_hash = obj['token_hash']
        self.refresh_token = obj['new_rt']
        self.save()


        ...
    
    def check_token_hash(self, token_):
        """returns true if given refresh token is same with the current refresh token"""
        # print(token_)
        hasher = hashlib.sha256()
        ''
        key = bytes(self.key, encoding='utf8')
        hasher.update(key)
        key_hash =  hasher.hexdigest()
        
        hasher.update(bytes(f'{self.token_salt}{key_hash}', encoding='utf8'))
        token_hash = hasher.hexdigest()

        return token_hash == token_

    

    def __str__(self):
        return f'{self.key[:10]}../{self.user.id}'


class TokenBlackList(models.Model):
    token = models.TextField(unique=True)
    date = models.DateField(auto_now_add=True)