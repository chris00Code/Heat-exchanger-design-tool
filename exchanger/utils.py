def get_available_class_names(module, base_class=None):
    class_names = []
    for name, obj in module.__dict__.items():
        if isinstance(obj, type) and \
                (base_class is None or issubclass(obj, base_class)) \
                and obj.__module__ == module.__name__:
            class_names.append(name)
    return class_names
