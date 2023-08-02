from rest_framework import serializers
from .models import CustomUser,Book
from rest_framework.authtoken.models import Token



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email','author_pseudonym']

    def create(self,validated_data):
        password=validated_data.get('password')
        user=CustomUser.objects.create(username=validated_data.get('username'),email=validated_data.get('email'),author_pseudonym=validated_data.get('author_pseudonym'))
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        token.save()
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