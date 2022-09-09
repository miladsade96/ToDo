from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterPage

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('api/v1/', include('accounts.api.v1.urls')),
    # path('api/v2/', include('accounts.api.v2.urls'))
]
