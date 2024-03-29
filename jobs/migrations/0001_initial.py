# Generated by Django 5.0 on 2024-01-01 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('min_salary', models.PositiveIntegerField(default=10)),
                ('max_salary', models.PositiveIntegerField()),
                ('salary_type', models.CharField(choices=[('monthly', 'Monthly'), ('yearly', 'Yearly'), ('hourly', 'Hourly')], max_length=10)),
                ('job_location', models.CharField(max_length=50)),
                ('job_posting_date', models.DateField(auto_now=True)),
                ('experience', models.CharField(choices=[('internship', 'Internship'), ('freshers', 'Freshers'), ('experienced', 'Experienced')], max_length=50)),
                ('required_skill', models.JSONField()),
                ('company_logo', models.URLField(blank=True, null=True)),
                ('employment_type', models.CharField(choices=[('full_time', 'Full Time'), ('contract', 'Contract'), ('internship', 'Internship')], max_length=50)),
                ('job_description', models.TextField()),
            ],
        ),
    ]
