
from django.urls import path
from . import views

urlpatterns = [
    path('create_survey/', views.create_survey, name='create_survey'),
    path('create_question/<int:survey_id>/', views.create_question, name='create_question'),
    path('create_answer_option/<int:question_id>/', views.create_answer_option, name='create_answer_option'),
    path('survey/<int:survey_id>/edit/', views.edit_survey, name='edit_survey'),
    path('answer_option/<int:option_id>/edit/', views.edit_answer_option, name='edit_answer_option'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('', views.dashboard, name='dashboard'),
    path('survey/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),
]