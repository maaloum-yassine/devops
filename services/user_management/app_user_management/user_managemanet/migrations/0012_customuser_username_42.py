# Generated by Django 4.2.16 on 2024-10-31 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managemanet', '0011_customuser_is_logged_2fa'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username_42',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
