from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    path('resources/', views.ResourceListCreateAPIView.as_view()),
    path('resources/<str:pk>/', views.ResourceRetrieveUpdateDestroyAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
