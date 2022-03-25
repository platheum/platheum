from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from tokens.models import Token
from wallets.models import Wallet
import hashlib
import crypt

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    hash = models.CharField(max_length=200, unique=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    # admin
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=True) # a superuser

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return f'User/{self.id}/'






# signals
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs) -> None:
    if created:
        # create |token|wallet
        Wallet.objects.create(owner=instance)
        token = Token.objects.create(user=instance)

        # generating salt
        token_obj = token.generate_rf()
        while Token.objects.filter(refresh_token=token_obj['new_rt']).first() is not None:
            token_obj = token.generate_rf()

        # saving values
        token.token_salt = token_obj['token_salt']
        token.token_hash = token_obj['token_hash']
        token.refresh_token = token_obj['new_rt']
        token.save()
        
        # generating user's hash (instance)
        hasher = hashlib.sha256()

        salt = crypt.mksalt(crypt.METHOD_SHA512)
        key = bytes(f'{instance.id}{instance.auth_token.pk}{salt}', encoding='utf8')
        hasher.update(key)
        hash =  hasher.hexdigest()

        instance.hash = hash
        instance.save()

