def handle_errors(func):
    """ Decorator to handle errors and collect them in a list. """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs), None
        except Exception as e:
            return None, str(e)
    return wrapper