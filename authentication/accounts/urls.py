from django.urls import path
from accounts.views import UserRegistrationView, LogInView, AllUserProfileView,UserProfileView, UserChangePasswordView,UserPasswordResetView, SendPasswordEmailView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name= 'register'),
    path('login/', LogInView.as_view(), name= 'login'),
    path('profile/', UserProfileView.as_view(), name= 'profile'),
    path('all-profile/', AllUserProfileView.as_view(), name= 'all-profile'),

    path('changepassword/', UserChangePasswordView.as_view(), name= 'changepassword'),
    path('send-reset-password-email/', SendPasswordEmailView.as_view(), name= 'send-email-reset-password'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name= 'reset-password'),    

]
