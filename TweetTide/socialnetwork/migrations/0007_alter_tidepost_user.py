# Generated by Django 4.2.2 on 2023-06-29 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialnetwork', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tidepost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tidepost', to=settings.AUTH_USER_MODEL),
        ),
    ]