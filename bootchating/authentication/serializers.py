from rest_framework import serializers
import lepl.apps.rfc3696
import re
from .models import UserProfile
import traceback
from django.contrib.auth.models import User

class UserProfileSerialzer(serializers.ModelSerializer):
	password = serializers.CharField()

	class Meta:
		model = UserProfile
		fields = ('email','mobile','password')

	def validate_email(self,value):
		email_validator = lepl.apps.rfc3696.Email()
		if email_validator(value):
		    raise serializers.ValidationError("Invalid email format")
		return value

	def validate_mobile(self,value):
		if not re.search('^[7-9][0-9]{9}$',value):
			raise serializers.ValidationError('Invalid mobile number')
		return value


	def create(self, validated_data):
		user = User.objects.create(username=validated_data['email'],password=validated_data['password'])
		validated_data['user'] = user
		validated_data.pop('password')
		return self.Meta.model.objects.create(**validated_data)

class ForgotPasswordSerializer(serializers.Serializer):
	email = serializers.CharField(required=True)

	def validate_email(self,value):
		email_validator = lepl.apps.rfc3696.Email()
		if email_validator(value):
		    raise serializers.ValidationError("Invalid email format")
		return value


class ResetPasswordSerializer(serializers.Serializer):
	oldpassword = serializers.CharField(required=True)
	newpassword = serializers.CharField(required=True)
	confirmpassword = serializers.CharField(required=True)

	def validate(self,value):
		if value.get('newpassword') == value.get('confirmpassword'):
			return value
		else:
			raise serializers.ValidationError({"error":'new and confirm password not matched'})



