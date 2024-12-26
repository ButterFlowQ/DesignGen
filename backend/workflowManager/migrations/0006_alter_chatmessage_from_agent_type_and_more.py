# Generated by Django 5.1.4 on 2024-12-26 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflowManager', '0005_alter_chatmessage_creation_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='from_agent_type',
            field=models.CharField(blank=True, choices=[('agent', 'REQUIREMENT'), ('user', 'USER')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='in_reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workflowManager.chatmessage'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='to_agent_type',
            field=models.CharField(blank=True, choices=[('agent', 'REQUIREMENT'), ('user', 'USER')], max_length=5, null=True),
        ),
    ]
