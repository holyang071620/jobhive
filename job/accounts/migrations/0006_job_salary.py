# Generated by Django 5.2 on 2025-04-25 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_job_title_job_company_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='salary',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
