from django.db import models

class EmailFile(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)  # Field to store the source or domain
    password = models.CharField(max_length=255)  # Field to store passwords

    def __str__(self):
        return self.name
