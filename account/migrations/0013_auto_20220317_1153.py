# Generated by Django 3.2.1 on 2022-03-17 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_customuser_is_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnos',
            name='introdaction',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='diagnos',
            name='suggestion',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
