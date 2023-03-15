from django.contrib import admin
from django.urls import path, include
from accounts import urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('accounts.urls')),

]
