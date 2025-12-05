from django.urls import path
from .views import Index, Login, Logout,users_list

app_name = 'users'

urlpatterns = [
    path('', Index, name='login'),
    path('login/', Index, name='login_redirect'), # Changed name slightly to avoid conflict 
    path('auth/user/', Login, name='user_login'),
    path('logout/', Logout, name='user_logout'),
    path('users/list/', users_list, name='users_list'),
    
]
