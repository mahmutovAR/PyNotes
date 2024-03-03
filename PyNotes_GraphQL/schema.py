from enum import Enum
from typing import Union
from urllib.parse import urljoin

import requests
from strawberry import enum, field, input, mutation, Schema, type
from strawberry.fastapi import GraphQLRouter

from WebPyNotes_settings.database_settings import DatabaseAPI


@type
class Note:
    """Text Note object type."""
    id: str
    title: str
    text: str | None
    created: str
    updated: str | None


@input
class NoteInput:
    """Text Note input object type."""
    id: str | None = field
    title: str | None = field
    text: str | None = field


@enum
class NoteErrorType(Enum):
    """Text Note errors."""
    NOTE_NOT_FOUND = "The note with given ID does not exist."
    NOTE_TITLE_IS_TAKEN = "A note with given title already exists."


@type
class NoteError:
    """Text Note error object type."""
    errorType: NoteErrorType
    err_id: str | None
    err_title: str | None
    err_text: str | None
    err_created: str | None
    err_updated: str | None


def convert_to_note_object(input_data: dict) -> Note:
    """Formats note data into Note object."""
    return Note(id=input_data['id'],
                title=input_data['title'],
                text=input_data['text'],
                created=input_data['created'],
                updated=input_data['updated'])


def convert_title_is_taken_error_object(input_data: dict) -> NoteError:
    """Formats note data into NoteError object."""
    return NoteError(errorType=NoteErrorType.NOTE_TITLE_IS_TAKEN,
                     err_id=input_data['id'],
                     err_title=input_data['title'],
                     err_text=input_data['text'],
                     err_created=input_data['created'],
                     err_updated=input_data['updated'])


@type
class NoteQuery:
    @field
    def all_notes(self) -> list[Note]:
        """Returns all notes from a collection."""
        all_notes_data = requests.get(DatabaseAPI.get_notes_schema()).json()
        return [convert_to_note_object(note)
                for note in all_notes_data['notes_all']]

    @field
    def count_notes(self) -> int:
        """Returns the total number of notes in the collection."""
        total_notes = requests.get(DatabaseAPI.get_total_notes_schema()).json()
        return total_notes['notes_total']

    @field
    def note_by_id(self, note_id: str) -> Union[Note, NoteError]:
        """Returns note data with the specified ID."""
        note_content = requests.get(urljoin(DatabaseAPI.get_note_by_id_schema(), note_id)).json()
        if 'note_content' in note_content:
            return convert_to_note_object(note_content['note_content'])
        return NoteError(errorType=NoteErrorType.NOTE_NOT_FOUND,
                         err_id=None,
                         err_title=None,
                         err_text=None,
                         err_created=None,
                         err_updated=None)

    @field
    def note_by_title(self, query_object: str) -> list[Note]:
        """Returns note data with the specified title field."""
        api_url = urljoin(DatabaseAPI.get_note_by_query_schema(), f'?field=title&object={query_object}')
        notes_by_title = requests.post(api_url).json()
        return [convert_to_note_object(note)
                for note in notes_by_title['notes_found']]

    @field
    def note_by_text(self, query_object: str) -> list[Note]:
        """Returns note data with the specified text field."""
        api_url = urljoin(DatabaseAPI.get_note_by_query_schema(), f'?field=text&object={query_object}')
        notes_by_text = requests.post(api_url).json()

        return [convert_to_note_object(note)
                for note in notes_by_text['notes_found']]


@type
class NoteMutations:
    @mutation
    def create_note(self, note_data: NoteInput) -> Union[Note, NoteError]:
        """Inserts note into the collection and returns its data."""
        inserted_note_data = requests.post(DatabaseAPI.get_notes_schema(),
                                           json={'title': note_data.title, 'text': note_data.text}).json()
        for status, inserted_note in inserted_note_data.items():
            if 'title_is_taken' in status:
                return convert_title_is_taken_error_object(inserted_note)
            return convert_to_note_object(inserted_note_data['note_inserted'])

    @mutation
    def update_note(self, note_data: NoteInput) -> Union[Note, NoteError]:
        """Updates a note data and returns it."""
        updated_note_data = requests.put(urljoin(DatabaseAPI.get_notes_schema(), note_data.id),
                                         json={'title': note_data.title, 'text': note_data.text}).json()
        for status, updated_note in updated_note_data.items():
            if 'title_is_taken' in status:
                return convert_title_is_taken_error_object(updated_note)
            return convert_to_note_object(updated_note_data['note_updated'])

    @mutation
    def delete_note(self, note_id: str) -> bool:
        """Deletes a note from the collection."""
        api_url_with_data_id = urljoin(DatabaseAPI.get_notes_schema(), note_id)
        api_response = requests.delete(api_url_with_data_id)
        return api_response.json()['note_deleted']


schema = Schema(query=NoteQuery, mutation=NoteMutations)
graphql_app = GraphQLRouter(schema)
