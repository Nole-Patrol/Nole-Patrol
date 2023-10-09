from django.db import models

class EmailFile(models.Model):
    name = models.CharField(max_length=255)
