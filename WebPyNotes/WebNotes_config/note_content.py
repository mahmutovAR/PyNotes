class NoteContent:
    """Class for interaction with data from database.
     Converts mongo collection object to the string values of note's ID, title and text."""
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
