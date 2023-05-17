from sys import argv as sys_argv

from WebNotes_config import NotesTemplates, NoteContent, NOTES_DB, TEST_DB, NotesMSG
from bson.objectid import ObjectId
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.shortcuts import render

if 'test' in sys_argv:
    DATABASE_ID = TEST_DB
else:
    DATABASE_ID = NOTES_DB

from .forms import TextNoteForm


def homepage(request):
    """This is homepage of the web application.
    The main functions and the number of saved notes are displayed."""
    total_notes = db_count_notes()
    context_data = {'total_notes': total_notes}
    return render(request, NotesTemplates.get_homepage_template(), context=context_data)


def create_note(request):
    """Displays page with creating form.
    If entered data is valid and note with entered title doesn't exist, inserts note into the collection.
    Otherwise, an error message will be displayed."""
    db_count_notes()
    if request.method == 'POST':
        new_note = TextNoteForm(request.POST)
        if new_note.is_valid():
            new_note_title = new_note.cleaned_data['note_title']
            new_note_text = new_note.cleaned_data['note_text']
            note_already_exists = db_find_single_note_data({'_title': new_note_title})
            if note_already_exists:
                context_data = {'new_note_data': new_note,
                                'note_title_exists': NoteContent(note_already_exists)}
                return render(request, NotesTemplates.get_create_template(), context=context_data)

            db_insert_note({'_title': new_note_title, '_text': new_note_text})
            total_notes = db_count_notes()
            context_data = {'app_message': NotesMSG.get_msg_note_inserted(),
                            'total_notes': total_notes}
            return render(request, NotesTemplates.get_homepage_template(), context=context_data)
        else:
            note_form_errors = [new_note.errors[field].as_text()
                                for field in new_note.errors]

            context_data = {'app_error': note_form_errors,
                            'new_note_data': new_note}
            return render(request, NotesTemplates.get_create_template(), context=context_data)
    else:
        new_note = TextNoteForm()
    context_data = {'new_note_data': new_note}
    return render(request, NotesTemplates.get_create_template(), context=context_data)


def view_all_notes(request):
    """Displays list of all notes from collection."""
    total_notes = db_count_notes()
    all_notes = db_get_all_notes_data()
    all_notes_from_db = [NoteContent(note_from_db)
                         for note_from_db in all_notes]
    notes_in_db = get_pagination_object(request, all_notes_from_db, 5)

    context_data = {'total_notes': total_notes,
                    'notes_in_db': notes_in_db}
    return render(request, NotesTemplates.get_all_notes_template(), context=context_data)


def get_pagination_object(request, input_data: list, rows_num: int) -> list or None:
    """Converts inputted data into pagination object."""
    if input_data:
        paginator = Paginator(input_data, rows_num)
        page_number = request.GET.get("page")
        return paginator.get_page(page_number)
    else:
        return None


def view_note_content(request, data_id: str):
    """Displays document content with given ID."""
    query_note = db_find_single_note_data({'_id': ObjectId(data_id)})
    context_data = {'note_content': NoteContent(query_note)}
    return render(request, NotesTemplates.get_note_content_template(), context=context_data)


def edit_note(request, data_id: str):
    """Displays page with form for editing note data.
    If edited data is valid and new title doesn't exist, updates note in the collection.
    Otherwise, an error message will be displayed."""
    note_id = {'_id': ObjectId(data_id)}
    note_to_edit = db_find_single_note_data(note_id)
    current_note = note_to_edit['_id']
    if request.method == 'POST':
        new_note_data = TextNoteForm(request.POST)
        if new_note_data.is_valid():
            new_note_title = new_note_data.cleaned_data['note_title']
            new_note_text = new_note_data.cleaned_data['note_text']
            note_already_exists = db_find_single_note_data({'_title': new_note_title})
            if not note_already_exists or note_already_exists['_id'] == current_note:
                db_update_note(note_id, {"$set": {'_title': new_note_title,
                                                  '_text': new_note_text}})
                total_notes = db_count_notes()
                context_data = {'app_message': NotesMSG.get_msg_note_edited(),
                                'total_notes': total_notes}
                return render(request, NotesTemplates.get_homepage_template(), context=context_data)

            elif note_already_exists['_id'] != current_note:
                context_data = {'editable_note': NoteContent(note_to_edit),
                                'note_title_exists': NoteContent(note_already_exists)}
                return render(request, NotesTemplates.get_edit_note_template(), context=context_data)
        else:
            note_form_errors = [new_note_data.errors[field].as_text()
                                for field in new_note_data.errors]
            context_data = {'app_error': note_form_errors,
                            'editable_note': NoteContent(note_to_edit)}
            return render(request, NotesTemplates.get_edit_note_template(), context=context_data)

    context_data = {'editable_note': NoteContent(note_to_edit)}
    return render(request, NotesTemplates.get_edit_note_template(), context=context_data)


def delete_note(request, data_id: str):
    """Removes document with given ID from the collection."""
    db_delete_note({'_id': ObjectId(data_id)})
    total_notes = db_count_notes()
    context_data = {'app_message': NotesMSG.get_msg_note_deleted(),
                    'total_notes': total_notes}
    return render(request, NotesTemplates.get_homepage_template(), context=context_data)


def search_note(request):
    """Displays page with searching form.
    Searches for the given expression in the titles and texts of the notes in the collection
    and returns the result grouped by category."""
    query_object = None
    found_in_titles = None
    found_in_texts = None
    total_notes = db_count_notes()

    if request.method == 'POST':
        query_object = request.POST.get('search_for')
        found_in_titles = db_find_notes_by_query({'_title': {"$regex": query_object, '$options': 'im'}})

        found_in_texts = db_find_notes_by_query({'_text': {"$regex": query_object, '$options': 'im'}})

    context_data = {'total_notes': total_notes,
                    'query_object': query_object,
                    'title_results': found_in_titles,
                    'text_results': found_in_texts}
    return render(request, NotesTemplates.get_search_note_template(), context=context_data)


def db_count_notes() -> int:
    """Additional function, counts documents in the collection."""
    try:
        notes_in_database = DATABASE_ID.count_documents({})
    except Exception:
        raise DatabaseError
    else:
        return notes_in_database


def db_find_single_note_data(query_obj: dict) -> dict:
    """Additional function, finds one document in the collection by given ID."""
    try:
        found_in_database = DATABASE_ID.find_one(query_obj)
    except Exception:
        raise DatabaseError
    return found_in_database


def db_insert_note(input_data: dict) -> None:
    """Additional function, inserts document into the collection."""
    try:
        DATABASE_ID.insert_one(input_data)
    except Exception:
        raise DatabaseError


def db_get_all_notes_data() -> 'Cursor object':
    """Additional function, returns all documents from the collection."""
    try:
        all_notes = DATABASE_ID.find({})
    except Exception:
        raise DatabaseError
    return all_notes


def db_update_note(input_id: dict, input_data: dict) -> None:
    """Additional function, updates document in the collection."""
    try:
        DATABASE_ID.update_one(input_id, input_data)
    except Exception:
        raise DatabaseError


def db_delete_note(input_data: dict) -> None:
    """Additional function, deletes document from the collection."""
    try:
        DATABASE_ID.find_one_and_delete(input_data)
    except Exception:
        raise DatabaseError


def db_find_notes_by_query(query_obj: dict) -> list:
    """Additional function, finds documents in the collection by given expression."""
    try:
        found_in_database = DATABASE_ID.find(query_obj)
    except Exception:
        raise DatabaseError
    else:
        query_result = [NoteContent(found_note)
                        for found_note in found_in_database]
    return query_result


def web_notes_server_error(request):
    """Renders page with Server Error message."""
    return render(request, NotesTemplates.get_server_error_template(), status=500)
