# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_hstore.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_slug', models.SlugField(null=True)),
                ('document_title', models.TextField(null=True, blank=True)),
                ('document_summary', models.TextField(help_text=b'This is the first parage of the first page, be default', null=True, blank=True)),
                ('page_count', models.IntegerField(null=True)),
                ('thumbnail', models.TextField(help_text=b'url for image thumbnail', null=True, blank=True)),
                ('metadata', django_hstore.fields.SerializedDictionaryField(help_text=b'Document metadata, as a dict', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document_Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection_name', models.TextField()),
                ('collection_slug', models.SlugField()),
                ('collection_description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_number', models.IntegerField(null=True)),
                ('page_text', models.TextField(help_text=b'This is the page full text', null=True, blank=True)),
                ('image', models.TextField(help_text=b'url for image', null=True, blank=True)),
                ('thumbnail', models.TextField(help_text=b'url for image thumbnail', null=True, blank=True)),
                ('page_dimensions', django.contrib.gis.db.models.fields.PolygonField(srid=97589, null=True, spatial_index=False)),
                ('orientation', models.CharField(help_text=b'V=vertical, H=horizontal. Or do we need 4 orientations?', max_length=1, null=True)),
                ('doc', models.ForeignKey(to='documents.Document')),
            ],
        ),
        migrations.CreateModel(
            name='PageWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_pk', models.IntegerField()),
                ('text', models.CharField(max_length=755, null=True, blank=True)),
                ('word_num', models.IntegerField(null=True)),
                ('line_num', models.IntegerField(null=True)),
                ('bbox', models.CharField(max_length=31, null=True, blank=True)),
                ('poly', django.contrib.gis.db.models.fields.PolygonField(srid=97589, null=True, spatial_index=False)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='document_collection',
            field=models.ForeignKey(to='documents.Document_Collection', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('doc', 'page_number')]),
        ),
    ]
