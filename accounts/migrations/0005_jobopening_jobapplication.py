# Generated by Django 5.0 on 2024-07-05 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_studentprofile_education'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobOpening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateField()),
                ('job_type', models.CharField(choices=[('off_campus', 'Off Campus'), ('on_campus', 'On Campus')], max_length=10)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=10)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_openings', to='accounts.instituteprofile')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='accounts.studentprofile')),
                ('job_opening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='accounts.jobopening')),
            ],
        ),
    ]
