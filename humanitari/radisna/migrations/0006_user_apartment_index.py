# Generated by Django 4.1.2 on 2022-10-11 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radisna', '0005_alter_user_home_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='apartment_index',
            field=models.CharField(blank=True, choices=[('a', 'a'), ('b', 'б')], max_length=1, null=True),
        ),
    ]
