# Generated by Django 5.1.4 on 2025-01-30 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orchestrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='versioneddocument',
            name='html_document',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
