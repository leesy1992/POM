# Generated by Django 2.1.11 on 2021-05-21 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0010_auto_20190722_1136'),
    ]

    operations = [
        
     
        migrations.AddField(
            model_name='splitresult',
            name='beforeLogin',
            field=models.TextField(null=True),
        ),

    ]
