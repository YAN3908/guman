# Generated by Django 4.1.2 on 2022-10-05 17:52

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radisna', '0007_alter_user_date_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_birth',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2022, 10, 5, 17, 52, 43, 903364))]),
        ),
    ]
