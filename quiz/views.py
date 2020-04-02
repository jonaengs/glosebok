import random

from django.contrib.auth.decorators import permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView
from rest_framework.generics import ListAPIView

from quiz.forms import QuizWordForm
from quiz.models import Language, Script, QuizWord
from quiz.serializers import ScriptSerializer, QuizWordSerializer


class QuizDetailView(DetailView):
    """
    On first entering the page, the user is presented with a simple form for specifying the details of the quiz.
    These are sent as query parameters: 'num_qws' (number of quizwords) and 'translate_to' (english or foreign)
    On detail form submission, the actual quiz is generated.
    """
    model = Language
    template_name = 'quiz/quiz_page.html'

    def get_context_data(self, **kwargs):
        ctx = super(QuizDetailView, self).get_context_data(**kwargs)
        language = self.object
        num_qws, translate_to = self.request.GET.get('num_qws'), self.request.GET.get('translate_to')

        if num_qws and translate_to:  # form has been filled out correctly and quiz can be generated
            all_qws = language.quizword_set.all()
            num_qws = min(int(num_qws), all_qws.count())  # dont sample more than there are elems in the set
            selected_qws = random.sample(list(all_qws), k=num_qws)
            ctx.update({
                'quizwords': selected_qws,
                'show_script': language.script_set.exists() and translate_to == 'foreign',
                'translate_to': translate_to,
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

    def get_context_data(self, *args, object_list=None, **kwargs):
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
    language_id = request.GET.get('language', "")
    scripts = Script.objects.filter(language__id=language_id)
    serializer = ScriptSerializer(scripts, many=True)
    return JsonResponse(serializer.data, safe=False)


class QuizWordAPI(ListAPIView):
    queryset = QuizWord.objects
    serializer_class = QuizWordSerializer

