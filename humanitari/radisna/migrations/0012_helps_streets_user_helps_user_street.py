# Generated by Django 4.1.2 on 2022-10-09 10:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('radisna', '0011_user_invalid_user_many_children_alter_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Helps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help', models.DateTimeField(default=datetime.datetime.now)),
                ('Check', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Streets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='helps',
            field=models.ManyToManyField(blank=True, related_name='helpmy', to='radisna.helps'),
        ),
        migrations.AddField(
            model_name='user',
            name='street',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_street', to='radisna.streets'),
            preserve_default=False,
        ),
    ]
