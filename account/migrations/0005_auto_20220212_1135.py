# Generated by Django 3.2.1 on 2022-02-12 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220211_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, default='', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='drugs',
            field=models.ManyToManyField(related_name='drugs', to='account.Drug'),
        ),
        migrations.AddField(
            model_name='category',
            name='diagnos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diagnos', to='account.diagnos'),
        ),
    ]
