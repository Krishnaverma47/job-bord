import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from user.models import User
from user.serializers import RefreshAccessTokenSerializer, ResetPasswordSerializer, SendEmailVerificationAgainSerializer, UserRegisterSerializer, UserLoginSerializer, VerifyEmailTokenSerializer
from user.utils import get_access_token_for_user, get_tokens_for_user
from user.email import send_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Uid : ", uid)
            send_email(user, uid, token)
            return Response({"data":serializer.data,"code":status.HTTP_201_CREATED,"status":True, "message":"Successfully registered 'Please check email to verify account.' "})
        return Response({"errors":serializer.errors,"code":status.HTTP_400_BAD_REQUEST,"status":False})
    
class VerifyEmailToken(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyEmailTokenSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['email_verification_token']
            uid = serializer.validated_data['uid']
            try:
                uid = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(id=uid)
                print("Varification Value : ", default_token_generator.check_token(user, token))
                if default_token_generator.check_token(user, token):
                    user.is_verified= True
                    user.save()
                    return Response({"code":status.HTTP_200_OK,"status":True,"message":"Email verified successfully."})
                else:
                    return Response({"code":status.HTTP_400_BAD_REQUEST,"status":False,"message":"Invalid token."})
            except Exception as e:
                return Response({"errors":str(e),"code":status.HTTP_400_BAD_REQUEST,"status":False})
    

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
    
class RefreshAccessToken(APIView):
    def post(self, request, *args, **kwargs):
        serializer =RefreshAccessTokenSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            refresh_token = serializer.validated_data['refresh_token']
            try:
                refresh_token_obj = RefreshToken(refresh_token)
                user = User.objects.get(id=refresh_token_obj['user_id'])
                token = get_access_token_for_user(user)
                return Response({"access_token":token,"code":status.HTTP_200_OK,"status":True ,"message":'New access token has been generated.'})
            except Exception as e:
                return Response({"errors":e,"code":status.HTTP_400_BAD_REQUEST,"status":False})
            
class SendEmailVerificationAgain(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendEmailVerificationAgainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = serializer.validated_data['email']
            user =  User.objects.get(email=email)
            if not user:
                return Response({"code":status.HTTP_400_BAD_REQUEST,"status":False,"message":"User not found."})
            if user.is_verified:
                return Response({"code":status.HTTP_400_BAD_REQUEST,"status":False,"message":"Your account is already verified."})
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            send_email(user, uid, token)
            return Response({"code":status.HTTP_200_OK,"status":True,"message":"Email has been sent to your email."})
        except Exception as e:
            return Response({"errors":str(e),"code":status.HTTP_400_BAD_REQUEST,"status":False,"message":"Some things went worng please try after some times."})
        
class ResetPassword(APIView):
    permission_classes =[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user and user.check_password(serializer.validated_data["old_password"]) :
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"code":status.HTTP_200_OK,"status":True,"message":"Password reset successfully."})
        return Response({"code":status.HTTP_400_BAD_REQUEST,"status":False,"message":"Your old password is incorrect. Please try again"})
    