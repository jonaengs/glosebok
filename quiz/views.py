from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView

from dal import autocomplete

from quiz.models import Language, Script


class LanguageQuizView(DetailView):
    model = Language
    template_name = 'quiz/language_quiz.html'

    def get_context_data(self, **kwargs):
        language = kwargs['object']
        ctx = super(LanguageQuizView, self).get_context_data(**kwargs)
        ctx.update({'quizwords': language.quizword_set.all()})
        return ctx


class ScriptAutocomplete(autocomplete.Select2QuerySetView, PermissionRequiredMixin):
    permission_required = 'quiz.add_quizword'

    def get_queryset(self):
        return Script.objects.filter(language__name=self.q)
