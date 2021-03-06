# Generated by Django 2.0.5 on 2018-07-26 09:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poll_app', '0002_auto_20180726_0353'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailid',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emailid',
            name='email_id',
            field=models.EmailField(max_length=254),
        ),
    ]
