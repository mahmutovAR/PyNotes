import json

import requests
from django.db import DatabaseError
from graphql_query import Argument, InlineFragment, Operation, Query, Variable

from .graphql_config import GraphqlAPI

Graphql_API = GraphqlAPI.get_graphql_api()
NOTE_FIElDS = ['id', 'title', 'text', 'created', 'updated']
ERROR_FIELDS = ['errorType', 'errId', 'errTitle', 'errText', 'errCreated', 'errUpdated']


def data_total_notes() -> int | None:
    """Counts notes in the collection."""
    query = Query(name='countNotes')
    operation = Operation(type='query',
                          queries=[query])
    try:
        response = requests.post(url=Graphql_API,
                                 json={"query": operation.render()})
    except Exception:
        raise DatabaseError
    else:
        total_notes = json.loads(response.content)
        return total_notes['data']['countNotes']


def data_all_notes() -> list | None:
    """Returns all notes from the collection."""
    query = Query(name='allNotes',
                  fields=NOTE_FIElDS)
    operation = Operation(type='query',
                          queries=[query])
    try:
        response = requests.post(url=Graphql_API,
                                 json={"query": operation.render()})
    except Exception:
        raise DatabaseError
    else:
        all_notes = json.loads(response.content)
        return all_notes['data']['allNotes']


def data_note_content(input_id: str) -> dict:
    """Returns note from the collection with specified ID."""
    note_id = Variable(name="noteId", type="String!")
    query = Query(name='noteById',
                  arguments=[Argument(name="noteId", value='$noteId')],
                  typename=True,
                  fields=[InlineFragment(type="Note", fields=NOTE_FIElDS),
                          InlineFragment(type="NoteError", fields=ERROR_FIELDS)])
    operation = Operation(type='query',
                          variables=[note_id],
                          queries=[query])
    variables_data = {'noteId': input_id}
    try:
        response = requests.post(url=Graphql_API,
                                 json={"query": operation.render(), 'variables': variables_data})
    except Exception:
        raise DatabaseError
    else:
        note_content = json.loads(response.content)
        if 'data' in note_content:
            return note_content['data']['noteById']
        elif 'note_not_found' in note_content:
            return note_content['data']['noteById']


def data_search_note_by_title(input_query: str) -> list | None:
    """Returns notes from the collection with a specified expression in 'title' field."""
    query_object = Variable(name="queryObject", type="String!")
    query = Query(name='noteByTitle',
                  arguments=[Argument(name="queryObject", value="$queryObject")],
                  fields=NOTE_FIElDS)
    operation = Operation(type='query',
                          variables=[query_object],
                          queries=[query])
    variables_data = {'queryObject': input_query}
    try:
        response = requests.post(url=Graphql_API,
                                 json={"query": operation.render(), 'variables': variables_data})
    except Exception:
        raise DatabaseError
    else:
        notes_by_title = json.loads(response.content)
        return notes_by_title['data']['noteByTitle']


def data_search_note_by_text(input_query: str) -> list | None:
    """Returns notes from the collection with a specified expression in 'text' field."""
    query_object = Variable(name="queryObject", type="String!")
    query = Query(name='noteByText',
                  arguments=[Argument(name="queryObject", value="$queryObject")],
                  fields=NOTE_FIElDS)
    operation = Operation(type='query',
                          variables=[query_object],
                          queries=[query])
    variables_data = {'queryObject': input_query}
    try:
        response = requests.post(url=Graphql_API,
                                 json={"query": operation.render(), 'variables': variables_data})
    except Exception:
        raise DatabaseError
    else:
        notes_by_text = json.loads(response.content)
        return notes_by_text['data']['noteByText']


def data_insert_note(input_title: str, input_text: str = None) -> dict:
    """Inserts note into the collection."""
    note_data = Variable(name="NoteInput", type="NoteInput!")
    query = Query(name="createNote",
                  arguments=[Argument(name="noteData", value="$NoteInput")],
                  typename=True,
                  fields=[InlineFragment(type="Note", fields=NOTE_FIElDS),
                          InlineFragment(type="NoteError", fields=ERROR_FIELDS)])
    operation = Operation(type="mutation",
                          variables=[note_data],
                          queries=[query])
    variables_data = {'NoteInput': {'title': input_title, 'text': input_text}}
    try:
        response = requests.post(url=Graphql_API,
                                 json={"query": operation.render(), 'variables': variables_data})
    except Exception:
        raise DatabaseError
    else:
        inserted_note = json.loads(response.content)
        return inserted_note['data']['createNote']


def data_update_note(note_id: str, input_title: str, input_text: str) -> dict | None:
    """Updates note in the collection."""
    note_data = Variable(name="NoteInput", type="NoteInput!")
    query = Query(name="updateNote",
                  arguments=[Argument(name="noteData", value="$NoteInput")],
                  typename=True,
                  fields=[InlineFragment(type="Note", fields=NOTE_FIElDS),
                          InlineFragment(type="NoteError", fields=ERROR_FIELDS)])
    operation = Operation(type="mutation",
                          variables=[note_data],
                          queries=[query])
    variables_data = {'NoteInput': {'id': note_id, 'title': input_title, 'text': input_text}}
    try:
        response = requests.post(url=Graphql_API,
                                 json={"query": operation.render(), 'variables': variables_data})
    except Exception:
        raise DatabaseError
    else:
        updated_note = json.loads(response.content)
        return updated_note['data']['updateNote']


def data_delete_note(input_id: str) -> bool:
    """Deletes note from the collection."""
    note_id = Variable(name="noteId", type="String!")
    query = Query(name="deleteNote",
                  arguments=[Argument(name='noteId', value='$noteId')])
    operation = Operation(type="mutation",
                          variables=[note_id],
                          queries=[query])
    variables_data = {'noteId': input_id}
    try:
        requests.post(url=Graphql_API,
                      json={"query": operation.render(), 'variables': variables_data})
    except Exception:
        raise DatabaseError
    else:
        return True
