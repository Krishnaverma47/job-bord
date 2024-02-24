from django.db.models import Q

SALARY_CHOICES = [
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
    ('hourly', 'Hourly'),
    ]

EXPERIENCE_CHOICES = [
    ('internship', 'Internship'),
    ('freshers', 'Freshers'),
    ('experienced', 'Experienced'),
    ]

JOB_TYPE_CHOICES = [
    ('full_time', 'Full Time'),
    ('contract', 'Contract'),
    ('internship', 'Internship'),
    ]


filters = {
    'job_title': lambda value: Q(job_title__icontains=value),
    'company_name': lambda value: Q(company_name__icontains=value),
    'min_salary': lambda value: Q(min_salary__gte=value),
    'max_salary': lambda value: Q(max_salary__lte=value),
    'job_location': lambda value: Q(job_location__icontains=value),
    'job_posting_date': lambda value: Q(job_posting_date__gte=(value)),
    'experience': lambda value: Q(experience=value),
    "employment_type": lambda value: Q(employment_type=value),
}
