# Generated by Django 3.2.2 on 2021-05-12 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MaxScore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('easy', models.IntegerField(default=0)),
                ('moderate', models.IntegerField(default=0)),
                ('hard', models.IntegerField(default=0)),
                ('unbeatable', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
