# Generated by Django 5.2.3 on 2025-07-12 20:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0013_vacancy_published_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='interviewresult',
            unique_together={('user', 'vacancy')},
        ),
    ]
