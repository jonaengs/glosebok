from django.contrib import admin

from quiz.models import Language, QuizWord

admin.site.register((Language, QuizWord))
