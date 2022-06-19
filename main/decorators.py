from main.types.types import ResponsePagination
import math


def pagination(_limit=24):
    def decorate(func):
        def wrap(*args, **kwargs):
            page = kwargs.get('page', 0)
            limit = kwargs.get('limit', _limit)
            kwargs.pop('page')
            if 'limit' in kwargs:
                kwargs.pop('limit')
            items, status_code = func(*args, **kwargs)
            if 'message' in items:
                return {'items': [], **items}, status_code

            total_entries = len(items)
            items = [items[i:i + limit] for i in range(0, len(items), limit)]
            total_pages = math.ceil(total_entries / limit)
            try:
                items = items[page]
            except IndexError:
                items = []
            response: ResponsePagination = {
                'items': items,
                'pagination': {
                    'per_page': limit,
                    'current_page': page,
                    'total_entries': total_entries,
                    'total_pages': total_pages
                }
            }
            return response, status_code
        wrap.__name__ = func.__name__
        return wrap
    return decorate
