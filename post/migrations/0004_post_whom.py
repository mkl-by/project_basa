# Generated by Django 2.1.1 on 2018-09-16 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20180916_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='whom',
            field=models.CharField(blank=True, choices=[('p', 'Питер'), ('m', 'Москва'), ('k', 'Краснодар')], max_length=30, null=True),
        ),
    ]
