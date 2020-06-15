# Generated by Django 2.1 on 2020-04-16 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_number', models.IntegerField(unique=True)),
                ('subject', models.CharField(max_length=125)),
            ],
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.DeleteModel(
            name='TeacherUser',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
