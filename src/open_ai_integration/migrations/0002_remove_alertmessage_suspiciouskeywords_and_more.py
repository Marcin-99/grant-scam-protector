# Generated by Django 4.1.4 on 2022-12-16 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('open_ai_integration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertmessage',
            name='suspiciousKeywords',
        ),
        migrations.AddField(
            model_name='suspiciouskeyword',
            name='alertMessage',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='open_ai_integration.alertmessage'),
            preserve_default=False,
        ),
    ]