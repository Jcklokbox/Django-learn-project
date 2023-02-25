from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('feedback/', send_message, name='feedback'),
    path('', HomePage.as_view(), name='home'),
    path('news/category/<int:category_id>/', NewsCategory.as_view(), name='category'),
    path('news/<int:pk>/', GetNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
]