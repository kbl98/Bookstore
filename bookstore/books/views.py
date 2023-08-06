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


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
class PostOnly(permissions.BasePermission) :  
    
    def has_permission(self, request, view):
        methods_list = ['GET', ]
        if request.method not in methods_list:
            return True
        
        return bool(request.user and request.user.is_superuser)

        

class AllUsers(APIView):
    """
    View to list all users in the system.
    Requires token authentication.
    Only admin users are able to access this view.
    """
   
    renderer_classes = [XMLRenderer, ]
    permission_classes=[PostOnly]

    def get(self, request, format=None):
        self.authentication_classes = [authentication.TokenAuthentication]
        self.permission_classes = [permissions.IsAdminUser]
        """
        Return a list of all users.
        """
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        if request.content_type == 'application/json':
            return JsonResponse(serializer.data,safe=False)
        if request.content_type == 'application/xml':
            return Response(serializer.data)
        return  JsonResponse(serializer.data,safe=False)
           
    
    def post(self, request, format=None):

        data=request.data.copy()
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserDetailsView(APIView):
    """
    User Details only viewable and changeable for  logged user himself
    
    """

    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, pk, format=None):
        user = CustomUser.objects.get(pk=pk)
        if user==self.request.user:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        return Response(status=405)

    def put(self, request, pk, format=None):
        user = CustomUser.objects.get(pk=pk)
        if user==self.request.user:
            serializer = CustomUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(status=405)

    def patch(self, request, pk, format=None):
        user = CustomUser.objects.get(pk=pk)
        if user==self.request.user:
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(status=405)
    
    def delete(self, request, pk, format=None):
        user = CustomUser.objects.get(pk=pk)
        if user:
            if user==self.request.user:
                user.delete()
                return Response(status=204)
            return Response({"message":"Not allowed to delete"})
        return Response(status=400)
        
    
class AllBooks(APIView):
     """
     Return a list of all books or filtered books based on query parameters.
     POST only for authenticated users
     """        
     permission_classes = [permissions.IsAuthenticated|ReadOnly]

     def get(self, request, format=None):
        title = request.GET.get('title', '')
        authorname=request.GET.get('author','')
        filtered_books = Book.objects.filter(title__icontains=title,author__author_pseudonym__icontains=authorname, )
        serializer = BookSerializer(filtered_books, many=True)

        if request.content_type == 'application/json':
            return JsonResponse(serializer.data,status=201,safe=False)
        if request.content_type == 'application/xml':
            return Response(serializer.data,status=201)
        return  JsonResponse(serializer.data,safe=False)
        
      
     def post(self, request, format=None):
        self.authentication_classes = [authentication.TokenAuthentication]
        data=request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class BookDetailsView(APIView):

    permission_classes = [permissions.IsAuthenticated|ReadOnly]

    """
    Get Details of Book.For ability to put,patch or delete the logged user has to be author of book
    """
    def get(self, request, pk, format=None):
        book = Book.objects.get(pk=pk)
        if book:
            serializer = BookSerializer(book)

            if request.content_type == 'application/json':
                return JsonResponse(serializer.data,safe=False)
            if request.content_type == 'application/xml':
                return Response(serializer.data)
            return JsonResponse(serializer.data,safe=False)
        return Response(status=204)
        

    def put(self, request, pk, format=None):

        #self.authentication_classes = [authentication.TokenAuthentication]

        book = Book.objects.get(pk=pk)
        if book:
            if book.author==self.request.user:
                serializer = BookSerializer(book, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    if request.content_type == 'application/json':
                        return JsonResponse(serializer.data,safe=False)
                    if request.content_type == 'application/xml':
                        return Response(serializer.data)
                return Response(serializer.errors, status=400)
        return Response(status=204)

    def patch(self, request, pk, format=None):

        #self.authentication_classes = [authentication.TokenAuthentication]

        book = Book.objects.get(pk=pk)
        if book:
            if book.author==self.request.user:
                serializer = BookSerializer(book, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    if request.content_type == 'application/json':
                        return JsonResponse(serializer.data,safe=False)
                    if request.content_type == 'application/xml':
                        return Response(serializer.data)
                return Response(serializer.errors, status=400)
        return Response(status=204)
    
    def delete(self, request, pk, format=None):

        #self.authentication_classes = [authentication.TokenAuthentication]

        book = Book.objects.get(pk=pk)
        if book:
            if book.author==self.request.user:
                book.delete()
                return Response(status=204)
            return Response({"message":"Not allowed to delete, not author"})
        return Response(status=400)
    
     

class LoginView(APIView):
    """
    This view should be accessible also for unauthenticated users, Login with username and password
    """
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
