# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_summary',
            field=models.TextField(help_text=b'This is the first parage of the first page, be default', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='page_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='page_text',
            field=models.TextField(help_text=b'This is the page full text', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='thumbnail',
            field=models.TextField(help_text=b'url for image thumbnail', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='image',
            field=models.TextField(help_text=b'url for image', null=True, blank=True),
        ),
    ]
