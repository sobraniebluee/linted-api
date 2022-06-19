class Error:
    @classmethod
    def server_error(cls, msg="Server error"):
        return {'message': str(msg)}, 500

    @classmethod
    def error_not_found(cls, msg='Not found', status_code=404):
        return {'message': msg}, status_code

    @classmethod
    def error_default(cls, msg, status_code):
        return {'message': msg}, status_code
