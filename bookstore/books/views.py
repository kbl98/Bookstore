from django.shortcuts import render
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import CustomUser
from .serializers import CustomUserSerializer,BookSerializer
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
class AllUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data=request.data.copy()
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserDetailsView(APIView):
    def get(self, request, pk, format=None):
        user = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        user = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk, format=None):
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        return Response(status=204)
    
class AllBooks(APIView):
     def get(self, request, format=None):
        """
        Return a list of all users.
        """
        AllBooks = AllBooks.objects.all()
        serializer = BookSerializer(AllBooks, many=True)
        return Response(serializer.data)
    
     def post(self, request, format=None):
        data=request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
     

class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data=request.data.copy()
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        login(request, user)
        token,_ = Token.objects.get_or_create(user=user)
        token.save()
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=202)
