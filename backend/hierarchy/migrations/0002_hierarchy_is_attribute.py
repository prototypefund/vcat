# Generated by Django 2.0.1 on 2018-03-18 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hierarchy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hierarchy',
            name='is_attribute',
            field=models.BooleanField(default=False),
        ),
    ]
