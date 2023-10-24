from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.utils.crypto import get_random_string
from cryptography.fernet import Fernet
import base64
import hashlib
from Nole_Patrol.settings import SECRET_KEY

def get_fernet_key():
    return base64.urlsafe_b64encode(hashlib.sha256(SECRET_KEY.encode()).digest())

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # This hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)

    # Adding related_name attributes to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="customuser",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="customuser",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def generate_email_verification_token(self):
        random_str = get_random_string(30)
        secret_key = settings.SECRET_KEY
        raw_token = f"{random_str}{secret_key}"
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        self.email_verification_token = hashed_token
        self.save()
        return random_str  # This is the token sent to the user's email for verification

class EmailFile(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)  # Field to store the source or domain
    password = models.CharField(max_length=255, default='temp_password')  # Field to store encrypted passwords
    
    def save(self, *args, **kwargs):
        self.password = self.encrypt_password(self.password)
        super().save(*args, **kwargs)

    def encrypt_password(self, password):
        cipher_suite = Fernet(get_fernet_key())
        encrypted_text = cipher_suite.encrypt(password.encode())
        return encrypted_text.decode()

    def decrypt_password(self, encrypted_password):
        cipher_suite = Fernet(get_fernet_key())
        decrypted_text = cipher_suite.decrypt(encrypted_password.encode())
        return decrypted_text.decode()

    def __str__(self):
        return self.name