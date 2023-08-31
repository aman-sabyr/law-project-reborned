from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def send_activation_code(self, code, email):
        msg = f'''yo dude this is ur code {code}'''
        return 0

    def _create(self, email, password, **extra_fields):
        # normalize email
        email = self.normalize_email(email)

        # generate activation or recovery code
        activation_code = get_random_string(5)
        extra_fields.update({'activation_code': activation_code})

        # save new user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        # sends activation code to whatsapp
        self.send_activation_code(email=email, code=activation_code)

        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, **extra_fields)


class User(AbstractBaseUser):
    name = models.CharField(max_length=32, verbose_name='имя')
    last_name = models.CharField(max_length=32, blank=True, verbose_name='фамилия')
    email = models.EmailField(blank=False, primary_key=True, verbose_name='электронная почта')
    phone_number = models.CharField(max_length=50, blank=False, unique=True, verbose_name='номер телефона')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=5, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name} {self.last_name} {self.email}'

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

