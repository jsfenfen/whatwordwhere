# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_document_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_slug',
            field=models.SlugField(null=True),
        ),
    ]
