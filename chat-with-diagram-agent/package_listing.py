import pkgutil
import inspect
import importlib
import diagrams

def list_all_classes(package):
    package_name = package.__name__
    for module_info in pkgutil.walk_packages(package.__path__, package_name + '.'):
        try:
            module = importlib.import_module(module_info.name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__.startswith(package_name):
                    if not name.startswith('_'):
                        print(f'{obj.__module__}.{name}')
        except ImportError:
            continue

# List all classes in 'diagrams' package
list_all_classes(diagrams)