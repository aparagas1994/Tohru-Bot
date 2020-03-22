from pkgutil import walk_packages, extend_path
import inspect

__all__ = []
__path__ = extend_path(__path__, __name__)

for loader, name, is_pkg in walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)