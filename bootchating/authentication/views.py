from .serializers import UserProfileSerialzer,ResetPasswordSerializer,ForgotPasswordSerializer
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.response import Response
import traceback
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import login,authenticate
import jwt
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.http.response import JsonResponse

from authentication.utils.email import trigger_email
import django_rq,base64

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER



def get_jwt_refresh_token(request):
	try:
		payload = jwt_payload_handler(request.user)
		token = jwt.encode(payload, settings.SECRET_KEY)
		return token
	except Exception as e:
		return (e)

def jwt_refresh_token(method):
	""" Decorator to pass refresh token in reponse """
	def wrapper(request, *args, **kwargs):
		token = get_jwt_refresh_token(request.request)
		response = method(request, *args, **kwargs)
		response.data['token'] = token
		return response
	return wrapper

class RegisterUser(APIView):
	serializer_class = UserProfileSerialzer
	permission_classes = (AllowAny,)

	def post(self,request):
		res = {}
		try:
			serializer = self.serializer_class(data=request.data)
			if serializer.is_valid():
				try:
					serializer.save()
					res = {"status":"success","message":"user created succefully"}
					return Response(res)
				except Exception as e:
					traceback.print_stack()
					res = {"status":"failed","message":str(e)}
					return Response(res)
			return Response(serializer.errors)
		except Exception as e:
			res = {"status":"failed","message":str(e)}
			return Response(res)


class LoginUser(APIView):
	permission_classes = (AllowAny,)

	def post(self,request):
		res = {}		
		try:
			email = request.data['username']
			password = request.data['password']
			user = User.objects.get(username=email, password=password)
			if user:
				try:
					payload = jwt_payload_handler(user)
					token = jwt.encode(payload, settings.SECRET_KEY)
					login(request, user)
					user = authenticate(username=email, password=password)
					res['token'] = token
					return Response(res)
				except Exception as e:
					raise e
			else:
				res = {
				    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
				return Response(res, status=status.HTTP_403_FORBIDDEN)
		except Exception as e:
			res = {'error': 'User does not exists!!'}
			return Response(res, status=status.HTTP_200_OK)


class ResetPassword(TemplateView):
	serializer_class = ResetPasswordSerializer
	permission_classes = (AllowAny,)
	template_name = 'resetpassword.html'

	def get_context_data(self, **kwargs):
		context = super(ResetPassword, self).get_context_data(**kwargs)
		return context

	def post(self,request):
		try:
			data = {}
			data['oldpassword'] = request.POST['oldpassword']
			data['newpassword'] = request.POST['new_password']
			data['confirmpassword'] = request.POST['confirm_password']	
			serializer = self.serializer_class(data=data)
			if serializer.is_valid():
				try:
					user = User.objects.get(password=request.POST['oldpassword'])
					if user:
						user.password = request.POST['new_password']
						user.save()
				except Exception as e:
					return JsonResponse({'success':False,"message":str(e)})
				return JsonResponse({'success':True,"message":"password has been reset successfully!!"})
			else:
				return JsonResponse({"error":serializer.errors})
		except Exception as e:
			raise e
		return JsonResponse({'success':"token"})

class ForgotPassword(TemplateView):
	serializer_class = ForgotPasswordSerializer
	permission_classes = (AllowAny,)
	template_name = 'forgotpassword.html'


	def get_context_data(self, **kwargs):
		context = super(ForgotPassword, self).get_context_data(**kwargs)
		return context


	def post(self,request):
		try:
			request_data = {}
			request_data['email'] = request.POST['email']
			serializer = self.serializer_class(data=request_data)
			if serializer.is_valid():

				data = {
			            "subject": "Password reset link",
			            "message": "You can reset your password from here",
			            "user": request.user.username,
			            "email_to": request.POST['email']
			            }
				trigger_email(data)
				return JsonResponse({'success':"email sent successfully!"})
			else:
				return Response(serializer.errors)

		except Exception as e:
			raise e
			return Response({'error':str(e)})


class UserProfile(APIView):
	permission_classes = (IsAuthenticated,)

	@jwt_refresh_token
	def get(self,request, *args, **kwargs):
		return Response({'test':"success"})



