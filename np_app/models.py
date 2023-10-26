from django.db import models

class EmailFile(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    breach_site = models.CharField(max_length=255)  # Field to store breach site
    password = models.CharField(max_length=255, null=True, blank=True)  # Field to store passwords

    def __str__(self):
        return self.name
