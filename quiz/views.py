from django.views.generic import DetailView

from quiz.models import Language


class LanguageQuizView(DetailView):
    model = Language
    template_name = 'quiz/language_quiz.html'
