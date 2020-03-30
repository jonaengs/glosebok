# Generated by Django 3.0.4 on 2020-03-30 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_language_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Language')),
            ],
        ),
        migrations.AddField(
            model_name='quizword',
            name='script',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Script'),
        ),
    ]
