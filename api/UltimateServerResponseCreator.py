class UltimateServerResponseCreator:
    def __init__(self, entity_name):
        self.entity_name = entity_name

    def create_base_response_object(self, data):
        return {
            'type': self.entity_name,
            'data': data
        }

    def create_base_error_response_object(self, error_message):
        return {
            'message': error_message,
        }

    def response_201(self, obj):
        return self.create_base_response_object(obj), 201

    def response_200(self, obj):
        return self.create_base_response_object(obj), 200

    def response_422(self, message: str = None):
        message = message or "Could not process entity"
        return self.create_base_error_response_object(message), 422

    def response_403(self, message: str = None):
        message = message or "Access denied"
        return self.create_base_error_response_object(message), 403

    def response_404(self, message: str = None):
        message = message or "Not found"
        return self.create_base_error_response_object(message), 404

    def response_500(self, message):
        return self.create_base_error_response_object(message), 500

