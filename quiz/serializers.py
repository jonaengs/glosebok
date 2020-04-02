from rest_framework import serializers

from quiz.models import Script, QuizWord


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = '__all__'


class QuizWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizWord
        fields = '__all__'
