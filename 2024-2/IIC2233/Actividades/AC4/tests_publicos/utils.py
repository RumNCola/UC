import threading
import functools


class FakeLock:
    def __init__(self) -> None:
        self._locked = False
        self.accessed = False
        self.blocking = True
        self.releases = 0

    def acquire(self, blocking=True):
        self.blocking = blocking
        if not self._locked:
            self.accessed = True
            self._locked = True
            return True

        if self._locked:
            return False

    def release(self):
        self.releases += 1
        if self._locked:
            self._locked = False
        return RuntimeError("release unlocked lock")

    def locked(self):
        return self._locked

    def __enter__(self, *args, **kwargs):
        self.acquire()
        return args, kwargs

    def __exit__(self, *args, **kwargs):
        self.release()
        return args, kwargs


def timeout(seconds=10, error_message=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if error_message is None:
                final_message = (
                    "El tests no finaliza dentro del tiempo máximo asignado."
                )
            else:
                final_message = error_message

            result = [Exception(final_message)]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e

            thread = threading.Thread(target=target, daemon=True)
            thread.start()
            thread.join(seconds)
            if isinstance(result[0], Exception):
                raise result[0]

            return result[0]

        return wrapper

    return decorator
