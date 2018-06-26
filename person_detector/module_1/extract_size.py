from flask import jsonify


class extract_size():
    def __init__(self, **kwargs):
        params = dict(kwargs)

    def _get_size_dictionary(self):
        size_dictionary = {
            'shoulder': 13,
            'chest': 15,
            'waist': 20,
            'inseam': 15
        }
        return jsonify(**size_dictionary)
