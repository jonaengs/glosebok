from django import forms

from quiz.models import QuizWord


class QuizWordForm(forms.ModelForm):
    class Meta:
        model = QuizWord
        exclude = ('datetime_added', )
        widgets = {
            'english': forms.TextInput(attrs={'autofocus': 'autofocus'})
        }
