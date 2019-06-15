from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	email = models.EmailField(max_length=100)
	mobile = models.CharField(max_length=12)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)


	def __str__(self):
		if self.email==None:
			return "email"
		return self.email


