# Generated by Django 4.2.16 on 2024-10-29 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managemanet', '0006_rename_code_verification_customuser_code_opt'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='active_2fa',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_email_verified',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
