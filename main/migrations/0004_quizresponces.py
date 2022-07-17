# Generated by Django 4.0.6 on 2022-07-17 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_quizanswer_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResponces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_emil', models.EmailField(max_length=50)),
                ('user_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_question_answer', to='main.quizquestion')),
                ('user_responce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_responce_answer', to='main.quizanswer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
