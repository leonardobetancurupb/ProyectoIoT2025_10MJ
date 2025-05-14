from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'sensors'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('detail/<int:pk>/', views.SensorDetailView.as_view(), name='detail'),
    path('manage/', views.SensorManageView.as_view(), name='manage'),
    path('create/', views.SensorCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.SensorEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.SensorDeleteView.as_view(), name='delete'),
    path('api/data/<int:sensor_id>/', views.get_sensor_data, name='api_data'),
    path('add-data/<int:sensor_id>/', login_required(views.add_sensor_data), name='add_data'),
]
