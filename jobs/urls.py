from django.urls import path
from jobs.views import JobView, RetriviewJob


urlpatterns = [
    path('job-post/', JobView.as_view(), name='job'),
    path('job-list/', RetriviewJob.as_view(), name='job-list'),
    path('job-list/<int:job_id>/', RetriviewJob.as_view(), name='job-retriview'),
]
