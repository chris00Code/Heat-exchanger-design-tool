import warnings


def get_available_class_names(module, base_class=None):
    class_names = []
    for name, obj in module.__dict__.items():
        if isinstance(obj, type) and \
                (base_class is None or issubclass(obj, base_class)) \
                and obj.__module__ == module.__name__:
            class_names.append(name)
    return class_names


def get_def_or_calc_value(defined_value, calc_value, default: str = 'defined', default_value=NotImplemented):
    if default == 'calculated':
        defined_value, calc_value = calc_value, default_value
    value = default_value
    if defined_value is default_value:
        if calc_value is not default_value:
            value = calc_value
    else:
        value = defined_value
        if calc_value is not default_value and defined_value != calc_value:
            warnings.warn(f'defined value is not calculated, {default} is returned')
    return value
