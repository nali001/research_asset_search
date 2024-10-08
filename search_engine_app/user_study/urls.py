from django.urls import path
from user_study import views

app_name = 'user_study'
urlpatterns = [
    path('', views.user_study_start, name='default_user_study'),  # Default URL

    path('register/', views.register, name="register_participant"),
    path('information_survey/', views.information_survey, name='information_survey'),
    path('pretest/', views.pretest, name='pretest'),
    path('guide/', views.guide, name='guide'),
    path('intro_step/', views.intro_step, name='intro_step'),
    path('task/', views.task, name='task'),
    path('posttest/', views.posttest, name='posttest'),
    path('task_assignment/', views.task_assignment, name='task_assignment'),
    # path('github_index_pipeline/', views.github_index_pipeline, name='github_index_pipeline'), 
    # path('api/', apis.welcome),
    # path('api/api_test/', apis.api_test),
    path('layout/', views.test_layout, name='test_layout'),
]
