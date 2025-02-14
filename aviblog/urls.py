from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
# from .views import post_new

app_name = 'aviblog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path("search/", views.search, name="search"),
    path('tag/<slug:tag_slug>/', views.post_list,  name='post_list_by_tag'),
    path('new/', views.post_new, name='post_new'),
    path('<slug:post>/', views.post_detail,name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('<int:post_id>', views.delete, name='delete'),
    
]
