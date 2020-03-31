from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView

from quiz.forms import QuizWordForm
from quiz.models import Language, Script, QuizWord
from quiz.serializers import ScriptSerializer


class LanguageQuizView(DetailView):
    model = Language

    def get_context_data(self, **kwargs):
        language = kwargs['object']
        ctx = super(LanguageQuizView, self).get_context_data(**kwargs)
        ctx.update({'quizwords': language.quizword_set.all()})
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


class QuizWordCreateView(CreateView):
    model = QuizWord
    form_class = QuizWordForm
    success_url = reverse_lazy('add_quizword')


@permission_required('quiz.add_quizword')
def get_scripts(request):
    language_id = request.GET.get('language', None)
    if not language_id:
        return JsonResponse({})
    scripts = Script.objects.filter(language__id=language_id)
    serializer = ScriptSerializer(scripts, many=True)
    return JsonResponse(serializer.data, safe=False)
