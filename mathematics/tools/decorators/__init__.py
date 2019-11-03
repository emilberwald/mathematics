def timeout(seconds):
    import queue
    import threading
    import functools
    import time

    def thread_function(q, f, *args, **kwargs):
        ret = f(*args, **kwargs)
        q.put_nowait(ret)

    def decorator(function):
        @functools.wraps(function)
        def wrap(*args, **kwargs):
            q = queue.Queue()

            t = threading.Thread(
                target=thread_function,
                args=(q, function) + args,
                kwargs=kwargs,
                daemon=True,
            )
            start = time.time()
            t.start()
            try:
                return q.get(True, seconds)
            except queue.Empty as e:
                end = time.time()
                raise TimeoutError(
                    f"TIMEOUT ({seconds}[s] < {end - start}[s]): [{function.__qualname__}]"
                ) from e

        return wrap

    return decorator
