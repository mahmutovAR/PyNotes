from sys import argv as sys_argv

from flask import Flask, request, jsonify

from WebPyNotes_settings.database_settings import DatabaseAPI
from models import NOTES_DB, TEST_DB

app = Flask(__name__)


if 'test' in sys_argv:
    DATABASE = TEST_DB
else:
    DATABASE = NOTES_DB


@app.get(DatabaseAPI.get_notes_api())
def rest_get_all_notes():
    """Returns all notes from a collection."""
    all_notes = DATABASE.db_get_all_notes()
    return jsonify({'notes_all': all_notes}), 200


@app.get(DatabaseAPI.get_total_notes_api())
def rest_get_total_notes():
    """Returns the total number of notes in the collection."""
    total_notes = DATABASE.db_count_notes()
    return jsonify({'notes_total': total_notes}), 200


@app.get(DatabaseAPI.get_note_by_id_api())
def rest_get_note(data_id):
    """Returns a note from the collection by the specified ID."""
    note_content = DATABASE.db_query_note_by_id(data_id)
    if note_content:
        return jsonify({'note_content': note_content}), 200
    return jsonify({'note_not_found': data_id}), 200


@app.post(DatabaseAPI.get_notes_api())
def rest_add_note():
    """Inserts note into the collection and returns its data."""
    if request.is_json:
        note_title = request.json['title']

        if DATABASE.db_note_title_is_taken(note_title):
            return jsonify({'title_is_taken': DATABASE.db_note_title_is_taken(note_title)}), 200

        note_text = request.json['text']
        note_inserted = DATABASE.db_insert_note(note_title, note_text)
        return jsonify({'note_inserted': note_inserted}), 201

    return {"error": "Request must be JSON"}, 415


@app.put(DatabaseAPI.get_note_by_id_api())
def rest_update_note(data_id):
    """Updates a note data and returns it."""
    if request.is_json:
        note_title = request.json['title']

        if DATABASE.db_note_title_is_taken(note_title, data_id):
            return jsonify({'title_is_taken': DATABASE.db_note_title_is_taken(note_title, data_id)}), 200

        note_text = request.json['text']

        updated_note = DATABASE.db_update_note(data_id, note_title, note_text)
        return jsonify({'note_updated': updated_note}), 201

    return {"error": "Request must be JSON"}, 415


@app.delete(DatabaseAPI.get_note_by_id_api())
def rest_delete_note(data_id):
    """Deletes a note from the collection."""
    DATABASE.db_delete_note(data_id)
    return jsonify({'note_deleted': True}), 200


@app.post(DatabaseAPI.get_note_by_query_api())
def rest_search_note():
    """Returns the search result for the given expression in the 'TITLE' and 'TEXT' fields."""
    query_field = request.args.get('field')
    query_object = request.args.get('object')

    if query_field.lower() == 'title':
        found = DATABASE.db_query_note_by_obj({query_field: {"$regex": query_object, '$options': 'im'}})
    elif query_field.lower() == 'text':
        found = DATABASE.db_query_note_by_obj({query_field: {"$regex": query_object, '$options': 'im'}})
    else:
        assert False, 'unexpected query field'

    return jsonify({'notes_found': found}), 200


@app.post(DatabaseAPI.get_test_api())
def add_test_data():
    """Inserts test data into the test collection.
    The number of test notes is specified in the request."""
    if request.is_json:
        notes_num = request.json['test_notes_num']
        DATABASE.db_insert_test_data(notes_num)
    return {"error": "Request must be JSON"}, 415


@app.delete(DatabaseAPI.get_test_api())
def delete_test_data():
    """Deletes all notes from the test collection."""
    DATABASE.db_delete_test_data()
    return jsonify({'test_notes_deleted': True}), 200


if __name__ == '__main__':
    app.run(debug=False)
