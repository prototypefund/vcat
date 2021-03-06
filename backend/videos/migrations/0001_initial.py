# Generated by Django 2.0.1 on 2018-03-13 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hierarchy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_code', models.CharField(max_length=32)),
                ('url', models.TextField(max_length=512)),
                ('thumbnail', models.CharField(max_length=256)),
                ('graphic_content', models.BooleanField()),
                ('name_en', models.CharField(max_length=256)),
                ('name_ar', models.CharField(max_length=256)),
                ('date', models.CharField(max_length=16)),
                ('time', models.CharField(max_length=16)),
                ('location', models.CharField(max_length=256)),
                ('status', models.IntegerField(default=0)),
                ('reviewed_by', models.CharField(max_length=16, null=True)),
                ('reviewed_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collection_tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hierarchy.Hierarchy')),
                ('violation_tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hierarchy.Hierarchy')),
                ('weapon_tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hierarchy.Hierarchy')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
