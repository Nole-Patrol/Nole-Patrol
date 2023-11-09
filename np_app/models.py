'''
Description: This file contains the code to create the EmailFile model. This
                model is used to store the data imported from the .txt files in
                the following directories:
                    np_app/Database/data/ComboLists
                    np_app/Database/data/Database Dumps
                    np_app/Database/data/databases
                The data is imported into the EmailFile model and associated SQLite
                database using Django's bulk_create() method to improve performance.
Author(s): Sarah Zeidan, Brian Arango, Caitlin Marie Grimes
Last Modified Date: 27 October 2023
Assumptions: For records to be successfully inserted into the database, we assume
             the data in the files is in the correct format (email:password) and
             that the data files are in the correct directories.
References: https://docs.djangoproject.com/en/4.2/topics/db/models/
'''

from django.db import models
from cryptography.hazmat.primitives.ciphers.aead import AESCCM

KEY = bytes.fromhex('59f055c39b5074dc7ea97abde24fc05a')
NONCE = bytes.fromhex('c2bad8b4a4536c8f0732e8c2be')
aesccm = AESCCM(KEY)

'''
Class Name: EmailFile(models.Model)
Description: This class contains the code to create the EmailFile model. This
             model is used to store the breach data imported from the .txt files
             including the email, the password, and the source of the breach. The
             passwords are encrypted before import using the encrypt_password() method.
Author(s): Sarah Zeidan, Brian Arango, Caitlin Marie Grimes
Last Modified Date: 27 October 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/topics/db/models/
'''
class EmailFile(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)  # Field to store breach site
    encrypted_password = models.CharField(max_length=255, null=True, blank=True)  # Field to store encrypted passwords
    
    def set_password(self, password):
        """
        Encrypts the password and stores the ciphertext.
        """
        self.encrypted_password = aesccm.encrypt(NONCE, password.encode(), None).hex()

    def check_password(self, password):
        """
        Decrypts the encrypted password and checks if it matches the provided password.
        """
        try:
            decrypted_password = aesccm.decrypt(NONCE, bytes.fromhex(self.encrypted_password), None).decode()
            return decrypted_password == password
        except Exception as e:
            return False

    def __str__(self):
        return self.name

'''
Class Name: RegisteredUser
Description: This model represents users who have registered to be notified if their email is found in the breached database. 
             Each entry in this model corresponds to a unique email address that has either been checked against the database 
             or has received a breach notification.
Fields: 
    - email: A unique email address of the user.
Methods:
    - __str__(): Returns the email address of the registered user.
Author(s): Brian Arango
Last Modified Date: 30 October 2023
Assumptions: Each email in this model is unique and corresponds to a single user.
References: https://docs.djangoproject.com/en/4.2/topics/db/models/
'''
class RegisteredUser(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    
    def __str__(self):
        return self.email
