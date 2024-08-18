from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0001_initial'),  # Ensure this line is present
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE SCHEMA IF NOT EXISTS content;
            """
        ),
    ]
