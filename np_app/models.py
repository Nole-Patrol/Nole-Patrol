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
from cryptography.fernet import Fernet #pip install cryptography
import hashlib, base64
from Nole_Patrol.settings import SECRET_KEY

'''
Function Name: get_fernet_key()
Description: This function returns the fernet key used to encrypt and decrypt
             the passwords in the EmailFile model.
Parameters: N/A
Return Value: base64 encrypted byte string
Author(s): Brian Arango
Last Modified Date: 27 October 2023
Assumptions: N/A
References: N/A
'''
def get_fernet_key():
    return base64.urlsafe_b64encode(hashlib.sha256(SECRET_KEY.encode()).digest())
    
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
    password = models.CharField(max_length=255, null=True, blank=True)  # Field to store passwords

    #def save(self, *args, **kwargs):
    #    self.password = self.encrypt_password(self.password)
    #    super().save(*args, **kwargs)

    '''
    Function Name: encrypt_password(self, password)
    Description: This function encrypts the password using the fernet key and
                 returns the encrypted password.
    Parameters: self, password
    Return Value: byte string
    Author(s): Brian Arango
    Last Modified Date: 27 October 2023
    Assumptions: N/A
    References: N/A
    '''    
    def encrypt_password(self, password):
        cipher_suite = Fernet(get_fernet_key())
        encrypted_text = cipher_suite.encrypt(password.encode())
        return encrypted_text.decode()
    
    '''
    Function Name: decrypt_password(self, encrypted_password)
    Description: This function decrypts the password using the fernet key and
                 returns the decrypted password.
    Parameters: self, encrypted_password
    Return Value: byte string
    Author(s): Brian Arango
    Last Modified Date: 27 October 2023
    Assumptions: N/A
    References: N/A
    ''' 
    def decrypt_password(self, encrypted_password):
        cipher_suite = Fernet(get_fernet_key())
        decrypted_text = cipher_suite.decrypt(encrypted_password.encode())
        return decrypted_text.decode()

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
