from rest_framework import serializers
from jobs.models import Job 

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('job_posting_date',)
    
    def validate(self, attrs):
        if attrs.get("min_salary") < 10:
            raise serializers.ValidationError("Minimum salary cannot be less than $ 10k")
        
        if attrs.get("max_salary") > 500:
            raise serializers.ValidationError("Maximum salary cannot be greater than $ 500k")
        
        if attrs.get("min_salary") > attrs.get("max_salary"):
            raise serializers.ValidationError("Minimum salary cannot be greater than maximum salary")
        return attrs
