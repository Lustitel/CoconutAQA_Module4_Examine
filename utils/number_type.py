def is_number(val):
    return isinstance(val, (int, float)) and not isinstance(val, bool)

def is_int(val):
    return isinstance(val, int) and not isinstance(val, bool)

def is_str(val):
    return isinstance(val, str)