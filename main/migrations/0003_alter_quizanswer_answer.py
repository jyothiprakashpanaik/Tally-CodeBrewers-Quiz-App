# Generated by Django 4.0.6 on 2022-07-17 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_delete_quizresponce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizanswer',
            name='answer',
            field=models.TextField(),
        ),
    ]
