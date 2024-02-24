from rest_framework import serializers
from jobs.models import ApplyJob, Job 

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

class ApplyJobSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField()
    class Meta:
        model = ApplyJob
        fields = ['job_id', 'resume']
        extra_kwargs = {
            'resume': {'write_only': True}
        }

    def validate_resume(self, value):
        allowed_extensions = ['pdf', 'html', 'txt', 'doc', 'docx']
        ext = value.name.split('.')[-1]
        if ext.lower() not in allowed_extensions:
            raise serializers.ValidationError("Invalid file format. Allowed formats are PDF, HTML, TXT, DOC, DOCX.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return super().validate(attrs)