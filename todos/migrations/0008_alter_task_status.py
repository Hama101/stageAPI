# Generated by Django 3.2.4 on 2021-07-05 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0007_auto_20210705_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[('To Do', 'To Do'), ('Doing', 'Doing'), ('Done', 'Done')], default='To Do', max_length=15, null=True),
        ),
    ]
