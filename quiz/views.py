import random

from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import JsonResponse, QueryDict
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView

from quiz.forms import QuizWordForm
from quiz.models import Language, Script, QuizWord
from quiz.serializers import ScriptSerializer


class LanguageQuizView(DetailView):
    model = Language

    def get(self, request, *args, **kwargs):
        num_qs, translate_to = request.GET.get('num_qs'), request.GET.get('translate_to')
        if num_qs and translate_to:
            self.ready = True
            self.num_qs = int(num_qs)
            self.translate_to = translate_to
        else:
            self.ready = False
        return super(LanguageQuizView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        language = kwargs['object']
        ctx = super(LanguageQuizView, self).get_context_data(**kwargs)
        if self.ready:
            quizwords = language.quizword_set.all()
            if len(quizwords) >= self.num_qs:
                quizwords = random.choices(quizwords, k=self.num_qs)
            ctx.update({
                'quizwords': quizwords,
                'show_script': language.script_set.exists(),
                'ready': self.ready,
                'translate_to': self.translate_to,
            })
        return ctx


class LanguageListView(ListView):
    model = Language


class QuizWordListView(ListView):
    model = QuizWord

    def get_queryset(self):
        """
        About query parameters: Multiple values of the same parameter type can be passed in two ways: separated by comma
        (?q=a,b) or as separate parameters (?q=a&q=b). This implementation uses the former, but I'm starting to think
        the latter is less ugly. To retrieve values passed by the lattter technique, GET.getlist() must be used instead
        of Get.get(), else only the last argument will be retrieved. Note that getlist() returns a list while get()
        returns a string. If comma-separation is used, getlist() will simply return a list ["a,b"] :(
        """
        query = self.request.GET
        if query and query.get('languages') is not None:  # "is not None" allows for empty argument
            languages = query.get('languages').split(",")
            return QuizWord.objects.filter(language__name__in=languages)  # ugly I know, but it's kinda fun right?
        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(QuizWordListView, self).get_context_data(**kwargs)
        ctx.update({'languages': Language.objects.all()})
        return ctx


class QuizWordCreateView(SuccessMessageMixin, CreateView):
    model = QuizWord
    form_class = QuizWordForm
    success_message = "%(english)s - %(foreign)s added successfully"

    def get_success_url(self):
        return reverse_lazy('add_quizword') + f"?language={self.object.language}&script={self.object.script}"


@permission_required('quiz.add_quizword')
def get_scripts(request):
    language_id = request.GET.get('language', None)
    if not language_id:
        return JsonResponse({})
    scripts = Script.objects.filter(language__id=language_id)
    serializer = ScriptSerializer(scripts, many=True)
    return JsonResponse(serializer.data, safe=False)
