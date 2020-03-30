from django.contrib import admin
from django.contrib.admin import TabularInline

from quiz.models import Language, QuizWord, Script


class ScriptInline(TabularInline):
    model = Script
    extra = 1


class LanguageAdmin(admin.ModelAdmin):
    inlines = [
        ScriptInline,
    ]


class QuizWordAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(QuizWordAdmin, self).get_form(request, obj, change, **kwargs)
        return form

    class Media:
        js = ('static/js/show_script_choices.js', )



admin.site.register(QuizWord, QuizWordAdmin)
admin.site.register(Language, LanguageAdmin)
