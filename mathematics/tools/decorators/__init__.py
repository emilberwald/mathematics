def timeout(seconds):
    """
    https://stackoverflow.com/a/48980413/3021108
    """
    from threading import Thread
    import functools

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = [Exception(f"TIMEOUT ({seconds}[s]): [{function.__qualname__}]")]

            def thread_function():
                try:
                    result[0] = function(*args, **kwargs)
                except Exception as call_exc:
                    result[0] = call_exc

            thread = Thread(target=thread_function)
            thread.daemon = True
            try:
                thread.start()
                thread.join(seconds)
            except Exception as join_exc:
                raise join_exc
            return_value = result[0]
            if isinstance(return_value, BaseException):
                raise return_value
            return return_value

        return wrapper

    return decorator
