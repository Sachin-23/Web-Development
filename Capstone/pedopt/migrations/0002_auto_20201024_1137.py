# Generated by Django 3.1.1 on 2020-10-24 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedopt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='adopted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adopted_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pet',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
