# Generated by Django 4.2.16 on 2024-11-09 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_managemanet', '0019_alter_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_42',
        ),
    ]
