from django.contrib import admin
from django.contrib.admin import TabularInline

from quiz.forms import QuizWordForm
from quiz.models import Language, QuizWord, Script


class ScriptInline(TabularInline):
    model = Script
    extra = 1


class LanguageAdmin(admin.ModelAdmin):
    inlines = [
        ScriptInline,
    ]


class QuizWordAdmin(admin.ModelAdmin):
    model = QuizWord

    class Media:
        js = ('js/show_hide_script_choices.js', )


admin.site.register(QuizWord, QuizWordAdmin)
admin.site.register(Language, LanguageAdmin)
