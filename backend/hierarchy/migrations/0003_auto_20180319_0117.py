# Generated by Django 2.0.1 on 2018-03-19 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hierarchy', '0002_hierarchy_is_attribute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hierarchy',
            name='name_ar',
        ),
        migrations.AlterField(
            model_name='hierarchy',
            name='name_en',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
