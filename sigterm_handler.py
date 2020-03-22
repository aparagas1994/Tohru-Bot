import sys

sigterm_functions = []


def register_sigterm_handler():
    def register_wrapper(func):
        sigterm_functions.append(func)
        return func
    return register_wrapper


def sigterm_handler(_signo, _stack_frame):
    for func in sigterm_functions:
        func()
    sys.exit(0)
