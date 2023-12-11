from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from sys import argv as sys_argv

from WebPyNotes.WebNotes_settings import NotesAPI
from database_settings import NOTES_DB, TEST_DB, format_fields

app = Flask(__name__)


API_URL = NotesAPI.get_api_url()
API_URL_data_id = NotesAPI.get_api_url_data_id()
API_URL_search = NotesAPI.get_api_url_search()
TEST_API_URL = NotesAPI.get_test_api_url()


if 'test' in sys_argv:
    DATABASE = TEST_DB
else:
    DATABASE = NOTES_DB


@app.get(API_URL)
def get_all_notes():
    """Returns all documents from collection and total number of the documents."""
    total_notes = DATABASE.get_count_of_all_docs()
    all_notes = DATABASE.get_all_docs_from_collection()
    all_notes_formatted = [format_fields(note)
                           for note in all_notes]
    output_data = {'total notes': total_notes, 'notes': all_notes_formatted}
    return jsonify(output_data), 200


@app.get(API_URL_data_id)
def get_note(data_id):
    """Returns document from the collection by given ID."""
    query_note = DATABASE.get_doc_from_collection({'_id': ObjectId(data_id)})
    if query_note:
        note_content = format_fields(query_note)
    else:
        note_content = 'Note not found'
    return jsonify({'note': note_content}), 200


@app.post(API_URL)
def add_note():
    """Adds new document into collection."""
    if request.is_json:
        new_note_title = request.json['note_title']
        new_note_text = request.json['note_text']

        note_already_exists = DATABASE.get_doc_from_collection({'title': new_note_title})
        if note_already_exists:
            return jsonify({'note_already_exists': format_fields(note_already_exists)}), 200

        inserted_note_id = DATABASE.insert_doc_into_collection({'title': new_note_title, 'text': new_note_text})
        return jsonify({'note_already_exists': False,
                        'total_notes': DATABASE.get_count_of_all_docs(),
                        'inserted_note_id': inserted_note_id}), 201

    return {"error": "Request must be JSON"}, 415


@app.put(API_URL_data_id)
def update_note(data_id):
    """Updates document in the collection."""
    if request.is_json:
        new_note_title = request.json['note_title']
        new_note_text = request.json['note_text']
        note_id = {'_id': ObjectId(data_id)}

        note_to_edit = DATABASE.get_doc_from_collection({'_id': ObjectId(data_id)})
        current_note_id = note_to_edit['_id']

        note_already_exists = DATABASE.get_doc_from_collection({'title': new_note_title})
        if not note_already_exists or note_already_exists['_id'] == current_note_id:
            DATABASE.update_doc_in_collection(note_id, {"$set": {'title': new_note_title,
                                                                 'text': new_note_text}})
            return jsonify({'note_already_exists': False, 'total_notes': DATABASE.get_count_of_all_docs()}), 201

        elif note_already_exists['_id'] != current_note_id:
            return jsonify({'note_already_exists': format_fields(note_already_exists)}), 200
    return {"error": "Request must be JSON"}, 415


@app.delete(API_URL_data_id)
def delete_note(data_id):
    """Deletes document from the collection."""
    DATABASE.delete_doc_from_collection({'_id': ObjectId(data_id)})
    return jsonify({'total_notes': DATABASE.get_count_of_all_docs()}), 200


@app.post(API_URL_search)
def search_note():
    """Returns the search result for the given expression in the title and text fields."""
    query_field = request.args.get('field')
    query_object = request.args.get('object')
    query = {query_field: {"$regex": query_object, '$options': 'im'}}
    found = DATABASE.find_docs_from_collection_by_query(query)
    return jsonify({'notes_found': found}), 200


@app.post(TEST_API_URL)
def add_test_data():
    """Additional test function, inserts test data into test collection.
    The number of test documents is specified in the request."""
    if request.is_json:
        notes_num = request.json['test_notes_num']
        DATABASE.insert_test_data(notes_num)
    return {"error": "Request must be JSON"}, 415


@app.delete(TEST_API_URL)
def delete_test_data():
    """Additional test function, deletes all documents from the collection."""
    DATABASE.delete_all_docs_from_collection()
    return jsonify({'result': 'database is empty'}), 200


if __name__ == '__main__':
    app.run(debug=False)
