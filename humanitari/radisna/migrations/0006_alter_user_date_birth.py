# Generated by Django 4.1.2 on 2022-10-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radisna', '0005_alter_user_date_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_birth',
            field=models.DateTimeField(),
        ),
    ]
