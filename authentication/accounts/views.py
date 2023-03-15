from rest_framework.response import Response
from rest_framework import status   
from rest_framework.views import APIView
from accounts.serializers import UserRegistrationSerializer, LogInSerializer, UserProfileSerializer, AllUserProfileSerializer, UserPasswordChangeSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User



# GENERATING TOKEN MANUALLY
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):

        serializer = UserRegistrationSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({
                'msg' : 'Registration Successful',
                'token' : token,
            }, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogInView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format = None):
        serializer = LogInSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            email =serializer.data.get('email')
            password =serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response ({
                    'token' : token,
                    'msg': 'Login Success.'
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'errors': {'non_field_errors':['Email or password is not valid']}
                    }, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status= status.HTTP_200_OK)

class AllUserProfileView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        users = User.objects.all()
        serializer = AllUserProfileSerializer(users, many = True)
        print(serializer, "snbdhbfsbab")
        return Response(serializer.data, status= status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request, format=None):
        serializer = UserPasswordChangeSerializer(data= request.data, context = {'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg' : 'Password changed successfully.'}, status= status.HTTP_200_OK)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        data = request.data
        print(data)
        serializer = SendPasswordResetEmailSerializer(data = request.data)
        if serializer.is_valid():
            print('data')
            return Response({
                'msg': 'Password reset link send. pLease check ur email'
            }, status= status.HTTP_200_OK)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,uid, token, format = None):
        serializer = UserPasswordResetSerializer(data = request.data, context= {'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg' : 'Password reset successfully'}, status=status.HTTP_200_OK)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
