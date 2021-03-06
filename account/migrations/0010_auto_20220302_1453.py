# Generated by Django 3.2.1 on 2022-03-02 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_review_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='profession',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_profession', to='account.profession'),
        ),
        migrations.AlterField(
            model_name='review',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_doctor', to=settings.AUTH_USER_MODEL),
        ),
    ]
