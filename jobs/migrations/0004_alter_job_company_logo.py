# Generated by Django 5.0 on 2024-02-17 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_job_employment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company_logo',
            field=models.URLField(null=True),
        ),
    ]
