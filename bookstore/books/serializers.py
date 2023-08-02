from rest_framework import serializers
from .models import CustomUser,Book

from django.contrib.auth import authenticate



class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email','author_pseudonym','password']

    def create(self,validated_data):
        password=validated_data.get('password')
        user=CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.author_pseudonym = validated_data.get('author_pseudonym', instance.author_pseudonym)
        return instance
    

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Book
        fields=["title","author","description","cover","price"]

    def create(self,validated_data):
        data=validated_data
        book=Book.objects.create(title=data.get("title"),author=data.get("author"),description=data.get("description"),cover=data.get("cover"),price=data.get("price"))
        book.save()
        return book
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author= validated_data.get('author', instance.author)
        instance.description= validated_data.get('description', instance.description)
        instance.cover= validated_data.get('cover', instance.cover)
        instance.price= validated_data.get('price', instance.price)
        return instance
    

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    
    

    def validate(self, validated_data):
        # Take username and password from request
       
        username = validated_data.get('username')
        password = validated_data.get('password')
        print(username)
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        self.user = user  
        return validated_data