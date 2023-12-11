from urllib.parse import urljoin

from WebNotes_settings import NotesTemplates, NotesMSG, NotesAPI
from django.core.paginator import Paginator
from django.shortcuts import render
from requests import delete as requests_delete
from requests import get as requests_get
from requests import post as requests_post
from requests import put as requests_put

from .forms import TextNoteForm

API_URL = NotesAPI.get_api_url_for_views()


def homepage(request) -> None:
    """This is homepage of the web application.
    The main functions and the number of saved notes are displayed."""
    api_response = requests_get(API_URL)
    all_notes = api_response.json()
    context_data = {'total_notes': all_notes['total notes']}
    return render(request, NotesTemplates.get_homepage_template(), context=context_data)


def create_note(request) -> None:
    """Displays page with creating form.
    If entered data is valid and note with entered title doesn't exist, inserts note into the collection.
    Otherwise, an error message will be displayed."""
    if request.method == 'POST':
        new_note = TextNoteForm(request.POST)
        template, data = get_data_to_render(new_note, 'POST',
                                            API_URL, NotesTemplates.get_create_template(),
                                            'new_note_data', NotesMSG.get_msg_note_inserted())
        return render(request, template, context=data)

    return render(request,
                  NotesTemplates.get_create_template(),
                  context={'new_note_data': TextNoteForm()})


def view_all_notes(request) -> None:
    """Displays list of all notes from collection."""
    api_response = requests_get(API_URL)
    all_notes_data = api_response.json()

    total_notes = all_notes_data['total notes']
    all_notes = all_notes_data['notes']
    notes_in_db = get_pagination_object(request, all_notes, 5)

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


def view_note_content(request, data_id: str) -> None:
    """Displays document content with given ID."""
    api_url_with_data_id = urljoin(API_URL, data_id)
    api_response = requests_get(api_url_with_data_id)
    query_note = api_response.json()

    note_content = query_note['note']
    context_data = {'note_content': note_content}
    return render(request, NotesTemplates.get_note_content_template(), context=context_data)


def edit_note(request, data_id: str) -> None:
    """Displays page with form for editing note data.
    If edited data is valid and new title doesn't exist, updates note in the collection.
    Otherwise, an error message will be displayed."""
    api_url_with_data_id = urljoin(API_URL, data_id)
    api_response = requests_get(api_url_with_data_id)
    note_to_edit = api_response.json()['note']
    if request.method == 'POST':
        new_note = TextNoteForm(request.POST)
        template, data = get_data_to_render(new_note, 'PUT',
                                            api_url_with_data_id, NotesTemplates.get_edit_note_template(),
                                            'editable_note', NotesMSG.get_msg_note_edited())
        return render(request, template, context=data)

    return render(request,
                  NotesTemplates.get_edit_note_template(),
                  context={'editable_note': note_to_edit})


def delete_note(request, data_id: str) -> None:
    """Removes document with given ID from the collection."""
    api_url_with_data_id = urljoin(API_URL, data_id)
    api_response = requests_delete(api_url_with_data_id)
    note_deleted = api_response.json()
    return render(request,
                  NotesTemplates.get_homepage_template(),
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
                       input_url: str, input_template: str,
                       tag_in_template: str, app_message: str) -> str and dict:
    """Returns result for note creating (or editing) functions.
    Checks if form data is valid and if note with inputted title already exists."""
    if form_data.is_valid():
        new_note_data = {
            'note_title': form_data.cleaned_data['note_title'],
            'note_text': form_data.cleaned_data['note_text']
        }

        if request_method.upper() == 'POST':
            api_response = requests_post(input_url, json=new_note_data)
        elif request_method.upper() == 'PUT':
            api_response = requests_put(input_url, json=new_note_data)
        else:
            assert False, 'unexpected request method'

        all_data = api_response.json()
        if all_data['note_already_exists']:
            return input_template, {tag_in_template: form_data,
                                    'note_title_exists': all_data['note_already_exists']}
        return NotesTemplates.get_homepage_template(), {'app_message': app_message,
                                                        'total_notes': all_data['total_notes']}
    else:
        note_form_errors = [form_data.errors[field].as_text()
                            for field in form_data.errors]
        return input_template, {'app_error': note_form_errors,
                                'new_note_data': form_data}
