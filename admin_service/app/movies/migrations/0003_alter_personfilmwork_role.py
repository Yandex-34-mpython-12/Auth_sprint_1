# Generated by Django 4.0.4 on 2023-05-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_create_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.CharField(choices=[('director', 'director'), ('writer', 'writer'), ('actor', 'actor')], max_length=20, null=True, verbose_name='role'),
        ),
    ]
