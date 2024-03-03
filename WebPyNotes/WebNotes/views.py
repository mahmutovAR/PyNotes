from WebPyNotes_settings import NotesTemplates, NotesMSG
from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import TextNoteForm, TITLE_MAX_LENGTH, TEXT_MAX_LENGTH

from WebPyNotes_settings.get_data import *


def view_index(request) -> None:
    """Displays homepage of the application.
    The main functions and the number of saved notes are displayed."""
    context_data = {'total_notes': data_total_notes()}
    return render(request, NotesTemplates.get_index_template(), context=context_data)


def view_add_note(request) -> None:
    """Displays page with note adding form.
    If entered data is valid and note with entered title doesn't exist, inserts note into the collection.
    Otherwise, an error message will be displayed."""
    initial_context = {'form_legend': 'Add new note to database',
                       'button_value': 'Save note',
                       'title_max': TITLE_MAX_LENGTH,
                       'text_max': TEXT_MAX_LENGTH}
    if request.method == 'POST':
        new_note = TextNoteForm(request.POST)

        template, context_data = get_data_to_render(new_note,
                                                    initial_context,
                                                    NotesTemplates.get_add_note_template(),
                                                    NotesMSG.get_msg_note_inserted())
        return render(request, template, context=context_data)

    return render(request, NotesTemplates.get_add_note_template(), context=initial_context)


def view_all_notes(request) -> None:
    """Displays list of all notes from the collection."""
    total_notes = data_total_notes()
    all_notes = data_all_notes()

    rows_per_page = 5
    notes_in_db, page_num = get_pagination_object(request, all_notes, rows_per_page)

    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)

    start_page_num = rows_per_page * (page_num-1) + 1

    context_data = {'total_notes': total_notes,
                    'notes_in_db': notes_in_db,
                    'start_page_num': start_page_num}

    return render(request, NotesTemplates.get_all_notes_template(), context=context_data)


def get_pagination_object(request, input_data: list, rows_num: int) -> list and int or None:
    """Converts inputted data into pagination object. Returns list of notes and pagination page number."""
    if input_data:
        paginator = Paginator(input_data, rows_num)
        page_number = request.GET.get("page")
        return paginator.get_page(page_number), page_number
    else:
        return None, 1


def view_note_content(request, data_id: str) -> None:
    """Displays note content with specified ID."""
    note_content = data_note_content(data_id)
    if 'errorType' in note_content:
        if note_content['errorType'] == 'NOTE_NOT_FOUND':
            return render(request, NotesTemplates.get_note_content_template(), context={'note_content': None})

    return render(request, NotesTemplates.get_note_content_template(), context={'note_content': note_content})


def view_edit_note(request, data_id: str) -> None:
    """Displays page with form for note data editing.
    If edited data is valid and new title doesn't exist, updates note in the collection.
    Otherwise, an error message will be displayed."""
    initial_context = {'form_legend': 'Edit note',
                       'button_value': 'Save changes',
                       'title_max': TITLE_MAX_LENGTH,
                       'text_max': TEXT_MAX_LENGTH}

    note_to_edit = data_note_content(data_id)

    if request.method == 'POST':
        new_note = TextNoteForm(request.POST)

        template, context_data = get_data_to_render(new_note,
                                                    initial_context,
                                                    NotesTemplates.get_edit_note_template(),
                                                    NotesMSG.get_msg_note_updated(),
                                                    data_id)
        return render(request, template, context=context_data)

    initial_context.update({'title_field': note_to_edit['title'], 'text_field': note_to_edit['text']})
    return render(request, NotesTemplates.get_edit_note_template(), context=initial_context)


def view_delete_note(request, data_id: str) -> None:
    """Removes note with specified ID from the collection."""
    data_delete_note(data_id)
    return render(request,
                  NotesTemplates.get_index_template(),
                  context={'app_message': NotesMSG.get_msg_note_deleted(),
                           'total_notes': data_total_notes()})


def view_search_note(request) -> None:
    """Displays page with searching form.
    Searches for the given expression in the title and text fields
    and returns the result grouped by category."""
    query_object = None
    found_in_titles = None
    found_in_texts = None

    if request.method == 'POST':
        query_object = request.POST.get('search_for')

        found_in_titles = data_search_note_by_title(query_object)
        found_in_texts = data_search_note_by_text(query_object)

    context_data = {'total_notes': data_total_notes(),
                    'query_object': query_object,
                    'title_results': found_in_titles,
                    'text_results': found_in_texts}
    return render(request, NotesTemplates.get_search_note_template(), context=context_data)


def web_notes_server_error(request) -> None:
    """Renders page with Server Error message."""
    return render(request, NotesTemplates.get_server_error_template(), status=500)


def get_data_to_render(form_data: 'TextNoteForm obj',
                       context: dict, template: str,
                       message: str, note_id: str = None) -> str and dict:
    """Returns template and content for 'add' or 'update' page.
    Also checks whether the entered data is correct and whether a note with the entered title exists.
    If data is valid and title is not taken, then the note will be inserted or updated.
    Otherwise, an error message will be displayed."""
    if form_data.is_valid():
        new_note_title = form_data.cleaned_data['note_title']
        new_note_text = form_data.cleaned_data['note_text']

        if note_id is None:
            operation_result = data_insert_note(new_note_title, new_note_text)
        else:
            operation_result = data_update_note(note_id, new_note_title, new_note_text)

        if 'errorType' in operation_result:
            if operation_result['errorType'] == 'NOTE_TITLE_IS_TAKEN':
                title_is_taken_data = {'id': operation_result['errId'],
                                       'title': operation_result['errTitle'],
                                       'text': operation_result['errText'],
                                       'created': operation_result['errCreated'],
                                       'updated': operation_result['errUpdated']}
                context.update(
                    {'title_field': new_note_title,
                     'text_field': new_note_text,
                     'title_is_taken': title_is_taken_data})
                return template, context

        context.update({'app_message': message,
                        'total_notes': data_total_notes()})
        return NotesTemplates.get_index_template(), context

    else:
        note_form_errors = [form_data.errors[field].as_text()
                            for field in form_data.errors]
        context.update({'app_error': note_form_errors,
                        'title_field': form_data.data['note_title'],
                        'text_field': form_data.data['note_text']})

        return template, context
