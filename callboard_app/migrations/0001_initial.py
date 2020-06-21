# Generated by Django 2.2.12 on 2020-06-21 12:38

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
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('text_of_announcement', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aut', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('announcement', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ann', to='callboard_app.Announcement')),
                ('author_of_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aut_com', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='announcement',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='announcement', to='callboard_app.Tag'),
        ),
    ]
