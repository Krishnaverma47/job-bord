from django.db import models
from jobs.utils import SALARY_CHOICES, EXPERIENCE_CHOICES, JOB_TYPE_CHOICES

# Create your models here.
class Job(models.Model):
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    min_salary = models.PositiveIntegerField(default=10)
    max_salary = models.PositiveIntegerField()
    salary_type = models.CharField(max_length=10, choices=SALARY_CHOICES)
    job_location = models.CharField(max_length=50)
    job_posting_date = models.DateField(auto_now=True)
    experience = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)
    required_skill = models.JSONField()
    company_logo = models.URLField(null=True)
    employment_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    job_description = models.TextField()
    
    def __str__(self):
        return self.job_title
    


