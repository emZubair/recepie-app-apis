from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    """Manager class to create users"""

    def create_user(self, email, password=None, **extra_fields):
        """ create user with given email & password """

        if not email:
            raise(ValueError('Email is required to create a new user'))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """ creates and saves new super user"""

        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User model using Email """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return "Name:{} email:{}".format(self.name, self.email)


class Tag(models.Model):
    """Tag recepie"""

    name = models.CharField(max_length=32)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
