from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from jobs.models import ApplyJob, Job
from rest_framework.permissions import IsAuthenticated
from jobs.serializers import ApplyJobSerializer, JobSerializer
from jobs.utils import filters

# Create your views here.

class JobView(APIView):
    def post(self, request, format=None):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"code":status.HTTP_201_CREATED,"status":True,"message":"Job created successfully."})
        return Response({"errors":serializer.errors,"code":status.HTTP_400_BAD_REQUEST,"status":False})
    
class RetriviewJob(APIView):
    def get(self, request, job_id=None, format=None):
        try:
            if job_id is None:
                jobs = Job.objects.all()
                try:
                    for key, condition in filters.items():
                        value = request.query_params.get(key)
                        if value is not None:
                            jobs = jobs.filter(condition(value))
                    serializer = JobSerializer(jobs, many=True)
                    return Response({"data":serializer.data,"code":status.HTTP_200_OK,"status":True,"message":"Job has been successfully."})
                except Exception as e:
                    return Response({"errors":str(e),"code":status.HTTP_400_BAD_REQUEST,"status":False, "message":"Unable to find the jobs list."})
            else:
                job = Job.objects.get(id=job_id)
                serializer = JobSerializer(job, many=False)
                return Response({"data":serializer.data,"code":status.HTTP_200_OK,"status":True,"message":"Job has been successfully."})
        except Exception as e:
            return Response({"errors":str(e),"code":status.HTTP_400_BAD_REQUEST,"status":False, "message":"Unable to find the jobs list."})
        
        
class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ApplyJobSerializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid():
                job_id = serializer.validated_data.get('job_id')
                job = Job.objects.get(id=job_id)
                resume = serializer.validated_data.get('resume')
                if ApplyJob.objects.filter(job_id=job_id, user_id=request.user).first():
                    return Response({"code":status.HTTP_400_BAD_REQUEST,"status":False, "message":"You have already applied for this job."})
                ApplyJob.objects.create(job=job, user=request.user, resume=resume)
                return Response({"data":{"job_title" : job.job_title},"code":status.HTTP_201_CREATED,"status":True,"message":"Job has been applied successfully."})
            else:
                return Response({"errors":serializer.errors,"code":status.HTTP_400_BAD_REQUEST,"status":False, "message":"Please provide respective value for job."})
        except Exception as e:
            return Response({"errors":str(e),"code":status.HTTP_400_BAD_REQUEST,"status":False, "message":"Some things went wrong. Please try again"})
