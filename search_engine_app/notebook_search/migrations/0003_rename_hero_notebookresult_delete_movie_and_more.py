# Generated by Django 4.0.5 on 2022-09-19 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebook_search', '0002_hero'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hero',
            new_name='NotebookResult',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
