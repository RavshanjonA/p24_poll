# Generated by Django 5.1.1 on 2024-09-17 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0012_alter_account_phone"),
    ]

    operations = [
        migrations.RunSQL("create extension if not exists pg_trgm"),

    ]
