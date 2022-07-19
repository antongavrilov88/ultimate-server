from config import api_version_str


def make_default_response_object():
    return {
        'jsonapi': {
            'version': api_version_str
        },
        'meta': {
            'copyright': 'AGwallet server',
            'authors': [
                'Anton Gavrilov'
            ]
        }
    }

