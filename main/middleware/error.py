class Error:
    @classmethod
    def server_error(cls, msg):
        return {'message': str(msg)}, 500
