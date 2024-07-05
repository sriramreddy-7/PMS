# Generated by Django 5.0 on 2024-07-05 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_instituteprofile_contact_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='branch_specialization',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='degree',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='profile_pics/'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='year_of_passout',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
