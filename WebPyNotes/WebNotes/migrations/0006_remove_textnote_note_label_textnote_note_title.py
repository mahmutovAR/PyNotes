# Generated by Django 4.1.5 on 2023-02-24 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebNotes', '0005_textnote_delete_note_delete_notedb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textnote',
            name='note_label',
        ),
        migrations.AddField(
            model_name='textnote',
            name='note_title',
            field=models.CharField(default='Note Title', help_text="Enter note's label", max_length=100, verbose_name="Note's title"),
        ),
    ]