from django.db import models
from django.db.models import DO_NOTHING, CASCADE


class Language(models.Model):
    name = models.CharField(max_length=64, unique=True)
    emoji = models.CharField(max_length=5, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Script(models.Model):
    # example: japanese has 3 scripts: katakana, hiragana and kanji
    name = models.CharField(max_length=64)
    language = models.ForeignKey(to=Language, on_delete=CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name', )


class QuizWord(models.Model):
    english = models.CharField(max_length=64)
    foreign = models.CharField(max_length=64)
    language = models.ForeignKey(to=Language, on_delete=DO_NOTHING)
    script = models.ForeignKey(to=Script, on_delete=DO_NOTHING, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.english = self.english.lower()
        return super(QuizWord, self).save(*args, **kwargs)

    def __str__(self):
        return self.language.name + ": " + self.english

    class Meta:
        ordering = ('english', )
