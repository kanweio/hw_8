# Generated by Django 4.1.3 on 2022-11-18 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.TextField()),
                ('posts', models.ManyToManyField(to='blogs.post')),
            ],
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
