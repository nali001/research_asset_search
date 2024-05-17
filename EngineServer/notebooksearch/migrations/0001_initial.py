# Generated by Django 4.0.5 on 2024-02-21 11:35

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContextSearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=240)),
                ('timestamp', models.CharField(max_length=60)),
                ('event', models.CharField(max_length=60)),
                ('query', models.TextField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='KaggleNotebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docid', models.CharField(max_length=240)),
                ('name', models.CharField(max_length=60)),
                ('source', models.CharField(max_length=60)),
                ('html_url', models.CharField(default='No html URL.', max_length=240)),
                ('description', models.TextField(default='No description.')),
                ('source_id', models.CharField(max_length=60)),
                ('file_name', models.CharField(max_length=60)),
                ('language', models.CharField(max_length=60)),
                ('num_cells', models.CharField(max_length=60)),
                ('summarization', models.TextField()),
                ('summarization_relevance', models.CharField(max_length=60)),
                ('summarization_confidence', models.CharField(max_length=60)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotebookDownloadParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docid', models.CharField(max_length=240)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotebookDownloadResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docid', models.CharField(max_length=240)),
                ('notebook_source_file', models.TextField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotebookSearchParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=60)),
                ('query', models.TextField()),
                ('filter', models.CharField(blank=True, max_length=60, null=True)),
                ('facet', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotebookSearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField()),
                ('facets', models.CharField(max_length=60)),
                ('num_hits', models.IntegerField()),
                ('num_pages', models.IntegerField()),
                ('current_page', models.IntegerField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QueryGenerationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=240)),
                ('timestamp', models.CharField(max_length=60)),
                ('event', models.CharField(max_length=60)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SummarizationScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('score', models.CharField(max_length=60)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AnnotatedNotebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docid', models.CharField(max_length=240)),
                ('name', models.CharField(max_length=60)),
                ('source', models.CharField(max_length=60)),
                ('html_url', models.CharField(default='No html URL.', max_length=240)),
                ('description', models.TextField(default='No description.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContextSearchLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=240)),
                ('timestamp', models.CharField(max_length=60)),
                ('event', models.CharField(max_length=60)),
                ('query', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NotebookDownloadLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=240)),
                ('timestamp', models.CharField(max_length=60)),
                ('event', models.CharField(max_length=60)),
                ('docid', models.CharField(max_length=240)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NotebookSearchLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=240)),
                ('timestamp', models.CharField(max_length=60)),
                ('event', models.CharField(max_length=60)),
                ('query', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QueryGenerationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=240)),
                ('timestamp', models.CharField(max_length=60)),
                ('event', models.CharField(max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=240)),
                ('research_interests', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelevancyFeedbackLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=240)),
                ('timestamp', models.CharField(max_length=60)),
                ('event', models.CharField(max_length=60)),
                ('query', models.TextField()),
                ('num_stars', models.CharField(max_length=60)),
                ('annotated_notebook', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RelevancyFeedbackLog', to='notebooksearch.annotatednotebook')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneratedQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=60)),
                ('queries', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=240, null=True), size=10)),
                ('context_search_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='generated_queries', to='notebooksearch.contextsearchlog')),
            ],
        ),
        migrations.CreateModel(
            name='CellContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_type', models.CharField(max_length=60)),
                ('cell_content', models.TextField()),
                ('context_search_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell_contents', to='notebooksearch.contextsearchlog')),
                ('query_generation_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell_contents', to='notebooksearch.querygenerationlog')),
            ],
        ),
    ]
