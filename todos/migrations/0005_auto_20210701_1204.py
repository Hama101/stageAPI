# Generated by Django 3.2.4 on 2021-07-01 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todos', '0004_alter_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='delay',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[('To Do', 'To Do'), ('Doing', 'Doing'), ('Done', 'Done')], max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
