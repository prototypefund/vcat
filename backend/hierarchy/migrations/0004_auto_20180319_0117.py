# Generated by Django 2.0.1 on 2018-03-19 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hierarchy', '0003_auto_20180319_0117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hierarchy',
            old_name='name_en',
            new_name='name',
        ),
    ]