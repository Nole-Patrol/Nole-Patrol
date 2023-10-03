from django.db import models

class LeakedCredential(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')
    username = models.TextField()
    source = models.TextField()
    password = models.TextField()
    domain = models.TextField(null=True, blank=True)