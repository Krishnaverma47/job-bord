from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserRegisterSerializer, UserLoginSerializer, VerifyEmailTokenSerializer
from user.utils import get_tokens_for_user
from user.email import send_email

# Create your views here.

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_email(serializer.validated_data['email'])
            return Response({"data":serializer.data,"code":status.HTTP_201_CREATED,"status":True, "message":"Successfully registered 'Please check email to verify account.' "})
        return Response({"errors":serializer.errors,"code":status.HTTP_400_BAD_REQUEST,"status":False})
    
class VerifyEmailToken(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyEmailTokenSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['email_verification_token']
            email = serializer.validated_data['email']
            decoded_token = jwt.decode(token, algorithms=["HS256"], verify=False)
            print("Token", decoded_token)

    

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data, many=False)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
            if user and  user.check_password(serializer.validated_data["password"]):
                if user.is_verified:
                    token = get_tokens_for_user(user)
                    return Response({"token":token,"code":status.HTTP_200_OK,"status":True ,"message":'LoggedIn successfully.'})
                else:
                    return Response({"code":status.HTTP_400_BAD_REQUEST,"status":False,"message":"Your account not verified.'Please verify your account.'"})
            else:
                return Response({"code":status.HTTP_400_BAD_REQUEST,"status":False,"message":'Invalid credentials.'})
        return Response({"errors":serializer.errors,"code":status.HTTP_400_BAD_REQUEST,"status":False})