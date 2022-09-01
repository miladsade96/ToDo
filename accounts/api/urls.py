from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt'))
]
