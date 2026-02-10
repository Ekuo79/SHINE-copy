from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ApplyView.as_view(), name='apply'),
    path('submit-survey/', views.SurveySubmitView.as_view(), name='submit_survey'),
]