# Generated by Django 2.0.1 on 2018-04-09 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_image_phash'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='phash',
            field=models.BigIntegerField(blank=True),
        ),
    ]
