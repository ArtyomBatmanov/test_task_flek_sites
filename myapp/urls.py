from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, OrganizationView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('organizations/', OrganizationView.as_view(), name='organizations'),
    path('users/', UserListView.as_view(), name='user-list'),

]
