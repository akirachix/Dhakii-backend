from django.urls import path
from .views import (
    questions, 
    ScreeningTestScoreListView, 
    ScreeningTestScoreDetailView, 
    AnswerListCreateView, 
    AnswerDetailView
)

urlpatterns = [
    path('questions/', questions, name='questions'), 
    path('questions/<int:question_id>/', questions, name='question_detail'),
    path('screeningtestscore/', ScreeningTestScoreListView.as_view(), name='screeningtestscore'),
    path('screeningtestscore/<int:pk>/', ScreeningTestScoreDetailView.as_view(), name='screeningtestscore_detail'),
    path('screeningtestscore/date/<int:year>/<int:month>/<int:day>/', ScreeningTestScoreListView.as_view(), name='screeningtestscore_date'),
    path('answers/', AnswerListCreateView.as_view(), name='answer_list_create'),
    path('answers/<int:pk>/', AnswerDetailView.as_view(), name='answer_detail'),
]

