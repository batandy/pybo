# Generated by Django 4.1 on 2022-09-26 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0013_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='templates/images/'),
        ),
    ]
