# Generated by Django 3.2.4 on 2021-07-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0014_alter_team_leader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]