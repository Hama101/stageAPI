# Generated by Django 3.2.4 on 2021-07-19 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0015_alter_team_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='todos.team')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('send_at', models.DateTimeField(auto_now_add=True)),
                ('body', models.CharField(max_length=5000)),
                ('chatRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todos.chatroom')),
            ],
        ),
    ]