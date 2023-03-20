from WebNotes_config import parse_configuration_file
from bson.objectid import ObjectId
from django.http import HttpResponseRedirect
from django.shortcuts import render
from pymongo import MongoClient

from .forms import NewNoteForm


config_data = parse_configuration_file()
mongo_client = MongoClient(config_data.get_database_client_host())
db_name = mongo_client[config_data.get_database_name()]
USER_NOTES = db_name['default_user']


class NoteContent:
    __slots__ = ['__note_id', '__note_title', '__note_text']

    def __init__(self, note_data):
        self.__note_id = note_data['_id']
        self.__note_title = note_data['_title']
        self.__note_text = note_data['_text']

    def get_note_id(self):
        return self.__note_id

    def get_note_title(self):
        return self.__note_title

    def get_note_text(self):
        return self.__note_text


def homepage(request):
    """This is homepage of the website.
    The number of passwords from each category (Card, Login, Note) and
    number of available data-files are displayed."""
    notes_in_database = USER_NOTES.count_documents({})
    context_data = {'total_notes': notes_in_database}
    return render(request, 'homepage.html', context=context_data)


def create_note(request):
    """Displays page with creating form. Creates new note and saves it in the database."""
    if request.method == 'POST':
        new_note = NewNoteForm(request.POST)
        new_note_title = request.POST.get("note_title")
        new_note_text = request.POST.get("note_text")
        if new_note.is_valid():
            new_note_title = new_note.cleaned_data['note_title']
            note_already_exists = USER_NOTES.find_one({"note_title": new_note_title})
            if note_already_exists:
                context_data = {'new_note_data': new_note,
                                'note_already_exists': note_already_exists}
                return render(request, 'note_create.html', context=context_data)
        USER_NOTES.insert_one({'_title': new_note_title, '_text': new_note_text}).inserted_id
        return HttpResponseRedirect('/all_notes')
    else:
        new_note = NewNoteForm()

    context_data = {'new_note_data': new_note,
                    'note_title_exists': None}
    return render(request, 'note_create.html', context=context_data)


def view_all_notes(request):
    all_notes_from_db = [NoteContent(note_from_db)
                         for note_from_db in USER_NOTES.find({})]

    context_data = {'all_db_notes': all_notes_from_db}
    return render(request, 'notes_all.html', context=context_data)


def view_note_content(request, record_id):
    query_note = USER_NOTES.find_one({'_id': ObjectId(record_id)})
    context_data = {'note_content': NoteContent(query_note)}
    return render(request, 'note_content.html', context=context_data)


def edit_note(request, record_id):
    """Displays page with form for editing description of uploaded earlier data-file."""
    note_id = {'_id': ObjectId(record_id)}
    note_to_edit = USER_NOTES.find_one(note_id)
    if note_to_edit:
        if request.method == 'POST':
            new_note_title = request.POST.get('note_title')
            new_note_text = request.POST.get('note_text')

            edit_title = {"$set": {"_title": new_note_title}}
            USER_NOTES.update_one(note_id, edit_title)

            edit_text = {"$set": {"_text": new_note_text}}
            USER_NOTES.update_one(note_id, edit_text)
            return HttpResponseRedirect('/all_notes')
        else:
            context_data = {'editable_note': NoteContent(note_to_edit)}
            return render(request, 'note_edit.html', context=context_data)
    else:
        return render(request, 'error.html', context='No data found..def edit_note')


def delete_note(request, record_id):
    note_id = {'_id': ObjectId(record_id)}
    note_to_delete = USER_NOTES.find_one(note_id)
    if note_to_delete:
        USER_NOTES.delete_one(note_id)
        return HttpResponseRedirect('/all_notes')
    else:
        return render(request, 'error.html', context='No data found..def delete_note')


def search_note(request):
    """Displays page with searching form. Searches password in the database and returns result grouped by category."""
    search_object = None
    if request.method == 'POST':
        search_object = request.POST.get('search_for')
    if search_object:
        search_title = USER_NOTES.find({'_title': {"$regex": f'.{search_object}.'}})
        search_text = USER_NOTES.find({'_text': {"$regex": f'.{search_object}.'}})

        all_found_titles = [NoteContent(found_note)
                            for found_note in search_title]

        all_found_texts = [NoteContent(found_note)
                           for found_note in search_text]

    else:
        all_found_titles = None
        all_found_texts = None

    context_data = {'search_object': search_object,
                    'title_results': all_found_titles,
                    'text_results': all_found_texts}
    return render(request, 'note_search.html', context=context_data)
