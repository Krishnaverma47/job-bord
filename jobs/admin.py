from django.contrib import admin
from jobs.models import Job

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ('id','job_title', 'company_name','min_salary','max_salary','salary_type', 'job_location', 'job_posting_date', 'experience','required_skill', 'company_logo', 'employment_type', 'job_description')
    list_filter = ('salary_type', 'experience', 'employment_type') 
    search_fields = ('job_title', 'company_name', 'job_description')
    list_editable = ('salary_type', 'experience', 'employment_type')
    readonly_fields = ('job_posting_date',)

admin.site.register(Job, JobAdmin)