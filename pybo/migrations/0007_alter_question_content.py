# Generated by Django 4.1 on 2022-08-26 07:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0006_auto_20220809_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
