# Generated by Django 3.2.5 on 2021-07-07 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='short_url',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
