# Generated by Django 5.0 on 2024-01-21 03:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='poses')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accuracy_score', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'ordering': ['-accuracy_score', 'created_at'],
            },
        ),
    ]