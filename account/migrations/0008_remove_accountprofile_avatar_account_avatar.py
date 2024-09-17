# Generated by Django 5.1.1 on 2024-09-17 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0007_accountprofile_avatar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="accountprofile",
            name="avatar",
        ),
        migrations.AddField(
            model_name="account",
            name="avatar",
            field=models.ImageField(default="avatar.jpeg", upload_to="avatars/"),
        ),
    ]
