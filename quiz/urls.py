from django.urls import path

from quiz.views import QuizDetailView, get_scripts, LanguageListView, QuizWordCreateView, QuizWordListView, \
    QuizWordAPI

urlpatterns = [
    path('', LanguageListView.as_view(), name='language_list'),
    path('words/', QuizWordListView.as_view(), name='quizword_list'),
    path('add/', QuizWordCreateView.as_view(), name='add_quizword'),

    # autocomplete view
    path('match-scripts/', get_scripts, name='get_scripts'),

    path('<slug:slug>/', QuizDetailView.as_view(), name='language_detail'),

    path('api/quizwords/', QuizWordAPI.as_view(), name='quizword_api'),
]
