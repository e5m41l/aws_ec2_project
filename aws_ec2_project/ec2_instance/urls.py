from django.urls import path
from .views import EC2InstanceCreateView

urlpatterns = [
    path('ec2/create/', EC2InstanceCreateView.as_view(), name='create-ec2-instance'),
]
