# Generated by Django 3.1.1 on 2021-07-15 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20210715_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='client_id',
            field=models.CharField(default='none', max_length=255),
        ),
    ]
