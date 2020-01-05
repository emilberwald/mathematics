def timeout(*, seconds, handler=None):
    import queue as _queue
    import threading as _threading
    import functools as _functools
    import time as _time
    import warnings as _warnings

    def thread_function(q, f, *args, **kwargs):
        ret = f(*args, **kwargs)
        q.put_nowait(ret)

    def decorator(function):
        @_functools.wraps(function)
        def wrap(*args, **kwargs):
            q = _queue.Queue()

            t = _threading.Thread(target=thread_function, args=(q, function) + args, kwargs=kwargs, daemon=True,)
            start = _time.time()
            t.start()
            try:
                return q.get(True, seconds)
            except _queue.Empty as e:
                end = _time.time()
                if handler:
                    _warnings.warn(f"TIMEOUT ({seconds}[s] < {end - start}[s]): [{function.__qualname__}]")
                    handler()
                else:
                    raise TimeoutError(f"TIMEOUT ({seconds}[s] < {end - start}[s]): [{function.__qualname__}]") from e

        return wrap

    return decorator
