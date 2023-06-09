# Generated by Django 4.1.3 on 2022-11-06 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_user_id_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('followings', models.ManyToManyField(blank=True, related_name='followings', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
