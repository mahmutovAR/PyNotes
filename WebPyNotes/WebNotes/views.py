from urllib.parse import urljoin

from WebNotes_settings import NotesTemplates, NotesMSG, NotesAPI
from django.core.paginator import Paginator
from django.shortcuts import render
from requests import delete as requests_delete
from requests import get as requests_get
from requests import post as requests_post
from requests import put as requests_put

from .forms import TextNoteForm, TITLE_MAX_LENGTH, TEXT_MAX_LENGTH

API_URL = NotesAPI.get_api_for_views()


def index(request) -> None:
    """This is homepage of the web application.
    The main functions and the number of saved notes are displayed."""
    api_response = requests_get(API_URL)
    all_notes = api_response.json()
    context_data = {'total_notes': all_notes['total notes']}
    return render(request, NotesTemplates.get_index_template(), context=context_data)


def add_note(request) -> None:
    """Displays page with note adding form.
    If entered data is valid and note with entered title doesn't exist, inserts note into the collection.
    Otherwise, an error message will be displayed."""
    initial_data = {'form_legend': 'Add new note to database',
                    'button_value': 'Save note',
                    'title_max': TITLE_MAX_LENGTH,
                    'text_max': TEXT_MAX_LENGTH}
    if request.method == 'POST':
        new_note = TextNoteForm(request.POST)

        template, context_data = get_data_to_render(new_note, 'POST',
                                                    initial_data,
                                                    NotesTemplates.get_add_note_template(),
                                                    NotesMSG.get_msg_note_inserted())
        return render(request, template, context=context_data)

    return render(request, NotesTemplates.get_add_note_template(), context=initial_data)


def view_all_notes(request) -> None:
    """Displays list of all notes from collection."""
    api_response = requests_get(API_URL)
    all_notes_data = api_response.json()

    total_notes = all_notes_data['total notes']
    all_notes = all_notes_data['notes']

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
    """Displays document content with given ID."""
    api_url_with_data_id = urljoin(API_URL, data_id)
    api_response = requests_get(api_url_with_data_id)
    query_note = api_response.json()

    context_data = {'note_content': query_note['note']}
    return render(request, NotesTemplates.get_note_content_template(), context=context_data)


def edit_note(request, data_id: str) -> None:
    """Displays page with form for editing note data.
    If edited data is valid and new title doesn't exist, updates note in the collection.
    Otherwise, an error message will be displayed."""
    initial_data = {'form_legend': 'Edit note',
                    'button_value': 'Save changes',
                    'title_max': TITLE_MAX_LENGTH,
                    'text_max': TEXT_MAX_LENGTH}

    api_url_with_data_id = urljoin(API_URL, data_id)
    api_response = requests_get(api_url_with_data_id)
    note_to_edit = api_response.json()['note']

    if request.method == 'POST':
        new_note = TextNoteForm(request.POST)

        template, context_data = get_data_to_render(new_note, 'PUT',
                                                    initial_data,
                                                    NotesTemplates.get_edit_note_template(),
                                                    NotesMSG.get_msg_note_updated(),
                                                    api_url_with_data_id)
        return render(request, template, context=context_data)

    initial_data.update({'title_field': note_to_edit['title'], 'text_field': note_to_edit['text']})
    return render(request, NotesTemplates.get_edit_note_template(), context=initial_data)


def delete_note(request, data_id: str) -> None:
    """Removes document with given ID from the collection."""
    api_url_with_data_id = urljoin(API_URL, data_id)
    api_response = requests_delete(api_url_with_data_id)
    note_deleted = api_response.json()
    return render(request,
                  NotesTemplates.get_index_template(),
                  context={'app_message': NotesMSG.get_msg_note_deleted(),
                           'total_notes': note_deleted['total_notes']})


def search_note(request) -> None:
    """Displays page with searching form.
    Searches for the given expression in the titles and texts of the notes in the collection
    and returns the result grouped by category."""
    query_object = None
    found_in_titles = None
    found_in_texts = None
    api_response = requests_get(API_URL)
    all_notes = api_response.json()

    if request.method == 'POST':
        query_object = request.POST.get('search_for')

        api_url_title_filed = f'{API_URL}search?field=title&object={query_object}'
        api_url_text_field = f'{API_URL}search?field=text&object={query_object}'

        found_in_titles_api = requests_post(api_url_title_filed)
        found_in_texts_api = requests_post(api_url_text_field)

        found_in_titles = found_in_titles_api.json()['notes_found']
        found_in_texts = found_in_texts_api.json()['notes_found']

    context_data = {'total_notes': all_notes['total notes'],
                    'query_object': query_object,
                    'title_results': found_in_titles,
                    'text_results': found_in_texts}
    return render(request, NotesTemplates.get_search_note_template(), context=context_data)


def web_notes_server_error(request) -> None:
    """Renders page with Server Error message."""
    return render(request, NotesTemplates.get_server_error_template(), status=500)


def get_data_to_render(form_data: 'TextNoteForm obj', request_method: str,
                       context: dict, template: str,
                       message: str, api_url: str = API_URL) -> str and dict:
    """Displays page with note adding form.
    If entered data is valid and note with entered title doesn't exist, inserts note into the collection.
    Otherwise, an error message will be displayed."""
    if form_data.is_valid():
        new_note_data = {'note_title': form_data.cleaned_data['note_title'],
                         'note_text': form_data.cleaned_data['note_text']}

        if request_method.upper() == 'POST':
            api_response = requests_post(API_URL, json=new_note_data)
        elif request_method.upper() == 'PUT':
            api_response = requests_put(api_url, json=new_note_data)
        else:
            assert False, 'unexpected request method'

        all_data = api_response.json()

        if all_data['note_already_exists']:
            context.update(
                {'title_field': new_note_data['note_title'],
                 'text_field': new_note_data['note_text'],
                 'note_already_exists': all_data['note_already_exists']})

            return template, context

        # context.update({'app_message': message,
        #                 'total_notes': all_data['total_notes']})
        context.update({'app_message': message,})
        return NotesTemplates.get_index_template(), context

    else:
        note_form_errors = [form_data.errors[field].as_text()
                            for field in form_data.errors]
        context.update({'app_error': note_form_errors,
                        'title_field': form_data.data['note_title'],
                        'text_field': form_data.data['note_text']})

        return template, context
