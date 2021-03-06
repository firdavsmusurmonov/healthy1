# Generated by Django 3.2.1 on 2022-03-25 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_diagnos_drugs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.FloatField(blank=True, max_length=150, null=True)),
                ('device', models.CharField(blank=True, choices=[('ios', 'Ios'), ('android', 'Android')], max_length=50, null=True)),
                ('fctoken', models.CharField(blank=True, max_length=150, null=True)),
                ('url', models.CharField(blank=True, max_length=150, null=True)),
                ('is_required', models.BooleanField(default=False)),
                ('version_name', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('man', 'Man'), ('woman', ' Woman')], max_length=50, null=True),
        ),
    ]
