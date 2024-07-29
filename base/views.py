from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from base.serializers import StudentProfileSerializer
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

from django.middleware.csrf import get_token

from base.validations import validate_username,validate_password
from rest_framework.exceptions import ValidationError
# students/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentRegistrationSerializer, StudentSerializer,StudentLoginSerializer
from .models import Student,Profile


class StudentRegistrationView(APIView):
    def get(self, request):
        d1 = Student.objects.all()
        s1 = StudentSerializer(d1, many=True)
        return Response(s1.data)

    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(csrf_exempt, name='dispatch')
# class StudentLoginView(View):
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             request.session.set_expiry(120)  # Set session to expire in 2 minutes

#             return JsonResponse({'message': 'Login successful'})
#         else:
#             return JsonResponse({'message': 'Invalid credentials'}, status=400)


# @method_decorator(csrf_exempt, name='dispatch')
class StudentLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request,"-----")
        data = request.data
        print(data)

        # Ensure that validate_username and validate_password are properly defined
        if not validate_username(data):
            raise ValidationError("Invalid username.")
        
        if not validate_password(data):
            raise ValidationError("Invalid password.")
        
        serializer = StudentLoginSerializer(data=data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)

             # Generate CSRF token
            csrf_token = get_token(request)
           
            session_id = request.session.session_key

            message = {
                "response": "Login successfully",
                "csrf_token": csrf_token,
                "session_id": session_id,
                "status":status.HTTP_200_OK

            }
           
            # request.session.set_expiry(15)
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response("serializer.errors", status=status.HTTP_400_BAD_REQUEST)
        


    # def post(self,request):
    #     data=request.data
    #     assert validate_username(data)
    #     assert validate_password(data)
    #     serializer = StudentLoginSerializer(data=data)
	# 	if serializer.is_valid(raise_exception=True):
	# 		user = serializer.check_user(data)
	# 		login(request, user)
	# 		return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class StudentProfileCreateView(APIView):
#     # authentication_classes = [BasicAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]

#     # @method_decorator(ensure_csrf_cookie)
#     def get(self,request):
#         s1=Profile.objects.all()
#         s2=StudentProfileSerializer(s1,many=True)
#         return Response(s2.data)

#     def post(self, request):
#         serializer = StudentProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Profile created successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         try:
#             profile = Profile.objects.get(pk=pk)
#         except Profile.DoesNotExist:
#             return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = StudentProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class StudentProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.all()
        serializer = StudentProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"message": "Profile created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)