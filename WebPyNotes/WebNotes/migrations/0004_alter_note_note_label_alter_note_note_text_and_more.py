# Generated by Django 4.1.5 on 2023-02-01 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebNotes', '0003_alter_notedb_db_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_label',
            field=models.CharField(help_text="Enter note's label", max_length=100, verbose_name="Note's label"),
        ),
        migrations.AlterField(
            model_name='note',
            name='note_text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='notedb',
            name='db_date',
            field=models.DateField(default='2023-02-01', verbose_name='Enter date in format YYYY-MM-DD'),
        ),
        migrations.AlterField(
            model_name='notedb',
            name='db_label',
            field=models.CharField(max_length=50, verbose_name='Enter datafile label'),
        ),
    ]
