from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutUsView.as_view(), name='aboutus'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
]
