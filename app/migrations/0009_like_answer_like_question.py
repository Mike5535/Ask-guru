# Generated by Django 4.0.4 on 2022-04-12 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_like_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.answer'),
        ),
        migrations.AddField(
            model_name='like',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.question'),
        ),
    ]
