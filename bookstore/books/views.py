from django.shortcuts import render
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import CustomUser,Book
from .serializers import CustomUserSerializer,BookSerializer
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_xml.parsers import XMLParser
from django.http import HttpResponse

class AllUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]
    renderer_classes = [XMLRenderer, ]
    #parser_classes = (XMLParser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        if request.content_type == 'application/json':
            return JsonResponse(serializer.data,safe=False)
        if request.content_type == 'application/xml':
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
        if user:
            if user==self.request.user:
                user.delete()
                return Response(status=204)
            return Response({"message":"Not allowed to delete"})
        return Response(status=400)
        
    
class AllBooks(APIView):
     def get(self, request, format=None):
        """
        Return a list of all users.
        """
        AllBooks = Book.objects.all()
        serializer = BookSerializer(AllBooks, many=True)
        if request.content_type == 'application/json':
            return JsonResponse(serializer.data,safe=False)
        if request.content_type == 'application/xml':
            return Response(serializer.data)
    
     def post(self, request, format=None):
        data=request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class BookDetailsView(APIView):
    def get(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        serializer = Book(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        if book:
            if book.author==self.request.user:
                book.delete()
                return Response(status=204)
            return Response({"message":"Not allowed to delete, not author"})
        return Response(status=400)
    
     

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
