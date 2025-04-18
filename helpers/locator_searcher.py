import sys
import os
import pkgutil
import inspect
import importlib.util

from utils import locators


class LocatorSearcher:
    def __init__(self, desired_locator):
        self.package = locators
        self.loc_target = desired_locator
        self.name = 'Not found'
        self.get()

    def __str__(self):
        return self.name

    def get_custom_modules(self):
        self.modules = [(importer.path, modname) for importer, modname, ispkg in
                        pkgutil.iter_modules(self.package.__path__) if not ispkg]

    def parse_modules(self):
        self.modules_parsed = [(os.path.join(path, name + '.py'), name + '.py') for path, name in self.modules]

    def load_module(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        return module

    def get(self):
        self.get_custom_modules()
        self.parse_modules()

        for file_path, module_name in self.modules_parsed:
            module = self.load_module(module_name, file_path)
            clsmembers = inspect.getmembers(module, inspect.isclass)

            for member in clsmembers:
                cls = member[-1]
                class_name = cls.__name__
                attr_names = [a for a in cls.__dict__ if not a.startswith('__')]
                for loc_name in attr_names:
                    locator = getattr(cls, loc_name)
                    if self.loc_target == locator:
                        self.name = (class_name + '.' + loc_name)
                        return
