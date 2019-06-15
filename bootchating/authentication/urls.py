from .views import RegisterUser,LoginUser,ResetPassword,ForgotPassword,UserProfile
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt


urlpatterns=[
    url(r"^signup/$",RegisterUser.as_view(),name="register-user"),
    url(r"^login/$",LoginUser.as_view(),name="login-user"),
    url(r"^forgotpssword/$",ForgotPassword.as_view(),name="forgor-pssword"),
    url(r"^resetpssword/$",ResetPassword.as_view(),name="reset-pssword"),
    url(r"^userprofile/$",UserProfile.as_view(),name="user-profile"),
]