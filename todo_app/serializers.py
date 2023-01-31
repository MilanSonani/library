from rest_framework.serializers import ValidationError
from .models import User, Book, BorrowUserBook
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'password']
        extra_kwargs = {
            'password':{'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
            validated_data['password'])
        user.first_name=validated_data['first_name']
        user.last_name=validated_data['last_name']
        user.role=validated_data['role']
        return user


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        if not email and not password:
            raise ValidationError({"Error": "Email or password is missing."})
        user = authenticate(username=email, password=password)
        if not user:
            raise ValidationError({"Error":"Invalid Login Credentials"})
        data['user'] = user
        return data


class LoginResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'token']

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)

        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }


class CreateBookSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    author = serializers.CharField()
    description = serializers.CharField()
    
    class Meta:
        model = Book
        fields = ['id', 'status', 'name', 'author', 'description']
        extra_kwargs = {
            'name':{'required': True},
            'author': {'required': True},
            'description': {'required': True}
        }


class BookResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author', 'description', 'status']


class UpdateBookSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    author = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.author = validated_data.get('author', instance.author)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class BorrowUserBookSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = BorrowUserBook
        fields = ('id', 'book', 'user')
