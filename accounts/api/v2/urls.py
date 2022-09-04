from django.urls import path, include


app_name = "api-v1"


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt'))
]
