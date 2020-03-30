from django import forms

from quiz.models import QuizWord


class QuizWordForm(forms.ModelForm):
    class Meta:
        model = QuizWord
        fields = '__all__'
