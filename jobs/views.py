from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from jobs.models import Job
from jobs.serializers import JobSerializer
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
