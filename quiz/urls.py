from django.urls import path

from quiz.views import LanguageQuizView, get_scripts, LanguageListView, QuizWordCreateView, QuizWordListView

urlpatterns = [
    path('', LanguageListView.as_view(), name='language_list'),
    path('words/', QuizWordListView.as_view(), name='quizword_list'),
    path('add/', QuizWordCreateView.as_view(), name='add_quizword'),

    # autocomplete view
    path('match-scripts/', get_scripts, name='get_scripts'),

    path('<slug:slug>/', LanguageQuizView.as_view(), name='language_detail'),
]
