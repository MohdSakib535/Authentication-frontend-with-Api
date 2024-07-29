from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Student, Profile

# students/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['username', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = Student(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
class StudentLoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def check_user(self,clean_data):
        request = self.context.get('request')

        student_data=authenticate(request,username=clean_data['username'],password=clean_data['password'])
        if not student_data:
            raise ValidationError('use not found')
        return student_data


class StudentAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            student = authenticate(request=self.context.get('request'), username=username, password=password)

            if not student:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['student'] = student
        return attrs


class StudentProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(),required=False)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'birth_date']

    # def create(self, validated_data):
    #     user = validated_data.pop('user')
    #     profile, created = Profile.objects.update_or_create(user=user, defaults=validated_data)
    #     return profile

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().update(instance, validated_data)



