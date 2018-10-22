# Generated by Django 2.0.1 on 2018-10-22 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0014_image_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='uploaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='base_href',
            field=models.CharField(blank=True, max_length=90),
        ),
        migrations.AlterField(
            model_name='image',
            name='verified',
            field=models.BooleanField(),
        ),
    ]
