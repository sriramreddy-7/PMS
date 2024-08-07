# Generated by Django 5.0 on 2024-07-07 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('JavaScript', 'JavaScript'), ('C++', 'C++'), ('Ruby', 'Ruby'), ('PHP', 'PHP'), ('HTML/CSS', 'HTML/CSS'), ('SQL', 'SQL'), ('Data Analysis', 'Data Analysis'), ('Machine Learning', 'Machine Learning'), ('UI/UX Design', 'UI/UX Design'), ('Project Management', 'Project Management'), ('Leadership', 'Leadership'), ('Communication', 'Communication'), ('Problem Solving', 'Problem Solving'), ('Teamwork', 'Teamwork')], max_length=100)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='accounts.studentprofile')),
            ],
        ),
    ]
