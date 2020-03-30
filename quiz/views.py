from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.views.generic import DetailView

from quiz.models import Language, Script
from quiz.serializers import ScriptSerializer


class LanguageQuizView(DetailView):
    model = Language
    template_name = 'quiz/language_quiz.html'

    def get_context_data(self, **kwargs):
        language = kwargs['object']
        ctx = super(LanguageQuizView, self).get_context_data(**kwargs)
        ctx.update({'quizwords': language.quizword_set.all()})
        return ctx


@permission_required('quiz.add_quizword')
def get_scripts(request):
    language_id = request.GET.get('language', None)
    if not language_id:
        return JsonResponse({})
    scripts = Script.objects.filter(language__id=language_id)
    serializer = ScriptSerializer(scripts, many=True)
    return JsonResponse(serializer.data, safe=False)

