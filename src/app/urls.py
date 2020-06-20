from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    path('patients/', views.PatientListCreateAPIView.as_view()),
    path('patients/<str:pk>/', views.PatientRetrieveUpdateDestroyAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
