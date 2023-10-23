from django.db import models
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet
import base64
import hashlib
from Nole_Patrol.settings import SECRET_KEY

def get_fernet_key():
    return base64.urlsafe_b64encode(hashlib.sha256(SECRET_KEY.encode()).digest())

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
