# Generated by Django 4.2.2 on 2023-06-28 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0002_alter_profile_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='linkedIn_link',
        ),
        migrations.AlterField(
            model_name='profile',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='socialnetwork.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='homepage_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
