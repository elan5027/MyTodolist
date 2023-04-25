from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserDataSerializer, LoginSerializer, UserEmailSerializer
from users.models import User
import jwt
from django.conf import settings


class SignupView(APIView):
    def post(self, request):
        serializer = UserDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request error"}, status=status.HTTP_409_CONFLICT)
        token = serializer.validated_data
        return Response(token, status=status.HTTP_200_OK)


#viewset rauter
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.filter(email=request.user.email).first()
        serializer = UserEmailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 공통적으로 유저가 로그인 된 상태 일 때 가능한 일이기 때문에 유저인증을 한다.
    def put(self, request):
        if request.data['email'] == request.user.email:
            user = User.objects.filter(email=request.data['email']).first()
            print(user)
            serializer = UserEmailSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

        return Response("put", status=status.HTTP_200_OK)

    def delete(self, request):
        username = request.user
        User.objects.filter(email=request.user.email).delete()
        return Response(f"{username}님 회원 탈퇴 완료", status=status.HTTP_200_OK)
