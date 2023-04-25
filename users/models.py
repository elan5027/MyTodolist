from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, name, age, gender, introduction, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have user name')
        if not age:
            raise ValueError('Users must have user age')
        if not gender:
            raise ValueError('Users must have user gender')
        if not introduction:
            raise ValueError('Users must have user introduction')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            age=age,
            gender=gender,
            introduction=introduction
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  email, introduction, name='admin', age=17, gender='M', password=None):
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            age=age,
            gender=gender,
            introduction=introduction
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(verbose_name='user name', max_length=20, unique=True)
    age = models.IntegerField(verbose_name='user age')
    gender = models.CharField(choices=GENDERS, max_length=2)
    introduction = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
