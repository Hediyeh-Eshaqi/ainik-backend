# Generated by Django 4.1.7 on 2023-08-15 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_alter_user_avatar_alter_user_firstname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalityComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.BooleanField()),
                ('age', models.IntegerField()),
                ('q1', models.IntegerField()),
                ('q2', models.IntegerField()),
                ('q3', models.IntegerField()),
                ('q4', models.IntegerField()),
                ('q5', models.IntegerField()),
                ('q6', models.IntegerField()),
                ('q7', models.IntegerField()),
                ('q8', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
