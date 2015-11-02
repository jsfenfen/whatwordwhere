# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_document_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='metadata',
            field=django_hstore.fields.SerializedDictionaryField(help_text=b'Document metadata, as a dict', null=True),
        ),
    ]
