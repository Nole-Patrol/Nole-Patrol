# Generated by Django 4.2.6 on 2023-10-26 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('np_app', '0002_emailfile_breach_site_emailfile_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailfile',
            name='breach_site',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
