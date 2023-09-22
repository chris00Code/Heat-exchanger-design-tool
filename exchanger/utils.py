import warnings


def get_available_class_names(module, base_class=None):
    """
    Get a list of class names defined in a module.

    This function searches a given module for defined classes and returns a list of their names.
    Optionally, you can specify a base class to filter the results and only include classes that are subclasses
    of the specified base class.

    Args:
        module (module): The Python module to search for class names.
        base_class (class, optional): The base class to filter the results. Default is None.

    Returns:
        list: A list of class names defined in the module.

    """
    class_names = []
    for name, obj in module.__dict__.items():
        if isinstance(obj, type) and \
                (base_class is None or issubclass(obj, base_class)) \
                and obj.__module__ == module.__name__:
            class_names.append(name)
    return class_names


def get_def_or_calc_value(defined_value, calc_value, default: str = 'defined', default_value=NotImplemented):
    """
    Get a value based on defined and calculated values.

    This function allows you to choose between a defined value, a calculated value.
    It returns the appropriate value based on the specified criteria.
    If only one value is defined, so the second value is equal to the default_value the value defined by default is returned.

    Args:
        defined_value (Any): The defined value.
        calc_value (Any): The calculated value.
        default (str, optional): The criteria for selecting the value ('defined', 'calculated', or 'default').
            Default is 'defined'.
        default_value (Any, optional): The default value to use if 'default' criteria is chosen. Default is NotImplemented.

    Returns:
        Any: The selected value based on the criteria.

    """
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
