# Generated by Django 3.1.7 on 2021-03-09 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20210309_0911'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.employee'),
        ),
    ]
