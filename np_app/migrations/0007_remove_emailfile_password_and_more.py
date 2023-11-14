# Generated by Django 4.2.5 on 2023-11-08 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('np_app', '0006_alter_emailfile_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailfile',
            name='password',
        ),
        migrations.AddField(
            model_name='emailfile',
            name='encrypted_password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]