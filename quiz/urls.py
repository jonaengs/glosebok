from django.urls import path
from django.views.generic import ListView

from quiz.models import Language
from quiz.views import LanguageQuizView

urlpatterns = [
    path('', ListView.as_view(model=Language), name='language_list'),
    path('<int:pk>/', LanguageQuizView.as_view(), name='language_quiz'),
]