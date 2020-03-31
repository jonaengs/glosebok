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
    model = QuizWord
    readonly_fields = ('datetime_added', )

    class Media:
        js = ('js/show_hide_script_choices.js', )


admin.site.register(QuizWord, QuizWordAdmin)
admin.site.register(Language, LanguageAdmin)
