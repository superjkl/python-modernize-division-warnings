import numpy
import warnings


def is_integer(x):
    t = type(x)
    return issubclass(t, int) or issubclass(t, long) or (
        numpy.issubdtype(x.dtype, numpy.integer) if issubclass(t, numpy.ndarray) else issubclass(t, numpy.integer))


def is_other_known(x):
    t = type(x)
    return is_integer(x) or issubclass(t, float) or issubclass(t, complex) or (
        numpy.issubdtype(x.dtype, numpy.inexact) if issubclass(t, numpy.ndarray) else issubclass(t, numpy.inexact))


def division_type(a, b):
    if is_integer(a) and is_integer(b):
        return 'int'
    elif is_other_known(a) and is_other_known(b):
        return 'float'
    else:
        return 'unknown'


def division_warning(a, b):
    type1, type2 = type(a), type(b)
    div_type = division_type(a, b)
    if div_type != 'unknown':
        warnings.warn("classic %s division" % (div_type,), Warning, stacklevel=3)
    else:
        warnings.warn("classic %s division for types %s /// %s" % (div_type, type1, type2), Warning,
                      stacklevel=3)


def warn_div(a, b):
    division_warning(a, b)
    return a / b


def warn_div_assign(a, b):
    division_warning(a, b)
    return b