def timeout(seconds):
    import queue as __queue
    import threading as __threading
    import functools as _functools
    import time as __time

    def thread_function(q, f, *args, **kwargs):
        ret = f(*args, **kwargs)
        q.put_nowait(ret)

    def decorator(function):
        @_functools.wraps(function)
        def wrap(*args, **kwargs):
            q = __queue.Queue()

            t = __threading.Thread(
                target=thread_function,
                args=(q, function) + args,
                kwargs=kwargs,
                daemon=True,
            )
            start = __time.time()
            t.start()
            try:
                return q.get(True, seconds)
            except __queue.Empty as e:
                end = __time.time()
                raise TimeoutError(
                    f"TIMEOUT ({seconds}[s] < {end - start}[s]): [{function.__qualname__}]"
                ) from e

        return wrap

    return decorator
