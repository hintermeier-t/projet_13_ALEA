# Generated by Django 3.1.7 on 2021-03-09 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("communication", "0002_auto_20210309_0911"),
        ("schedule", "0002_auto_20210309_0911"),
        ("authentication", "0002_remove_employee_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Employee",
        ),
    ]
