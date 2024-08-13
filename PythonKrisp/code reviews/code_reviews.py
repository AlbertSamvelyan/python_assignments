

def get_value(data, key, default, lookup=None, mapper=None):
    """
    Finds the value from data associated with key, or default if the
    key isn't present.
    If a lookup enum is provided, this value is then transformed to its
    enum value.
    If a mapper function is provided, this value is then transformed
    by applying mapper to it.
    """
    # Use return_value=data.get(key, default) instead in order to avoid KeyError Exceptions.
    return_value = data[key]
    if return_value is None or return_value == "":
        return_value = default
    if lookup:
        return_value = lookup[return_value]
    if mapper:
        return_value = mapper(return_value)
    return return_value

def ftp_file_prefix(namespace):
    """
    Given a namespace string with dot-separated tokens, returns the
    string with
    the final token replaced by 'ftp'.
    Example: a.b.c => a.b.ftp
    """
    # No need to split with "." and then agan join with "." here.
    # Instead the index of the last dot can be found with 'rindex' method and 
    # 'ftp' can be added to string starting from that position.
    return ".".join(namespace.split(".")[:-1]) + '.ftp'

def string_to_bool(string):
    """
    Returns True if the given string is 'true' case-insensitive,
    False if it is
    'false' case-insensitive.
    Raises ValueError for any other input.
    """
    # Please use lower() method at the begining once, 
    # then check the result, e.g lower_str = string.lower(), then if lower_str == 'true'...e.t.c.
    if string.lower() == 'true':
        return True
    if string.lower() == 'false':
        return False
    # Unclear error message will be displayed, if the string is empty, i.e
    # 'String    is neither true nor false'
    # Change message to something like: "String should be 'true' or 'false'"
    # or add double quotes to existing message to make it more clear, i.e:
    # 'String "   " is neither true nor false'(Note that it is visible here that string is empty).
    raise ValueError(f'String {string} is neither true nor false')

# Avoid using names that shadow built-in names 
def config_from_dict(dict):
    """
    Given a dict representing a row from a namespaces csv file,
    returns a DAG configuration as a pair whose first element is the
    DAG name
    and whose second element is a dict describing the DAG's properties
    """

    # In order to avoid KeyError exceptions when accessing data from dict with 'Namespace' or 'Airflow Dag'
    # key, please use the "getValue" method here.
    namespace = dict['Namespace']
    return (dict['Airflow DAG'],
        {"earliest_available_delta_days": 0,
         "lif_encoding": 'json',
         "earliest_available_time": get_value(dict, 'Available Start Time', '07:00'),
         "latest_available_time": get_value(dict, 'Available End Time', '08:00'),
         "require_schema_match": get_value(dict, 'Requires Schema Match', 'True', mapper=string_to_bool),
         "schedule_interval": get_value(dict, 'Schedule', '1 7 * * * '),
         # What is DeltaDays here?
         "delta_days": get_value(dict, 'Delta Days', 'DAY_BEFORE', lookup=DeltaDays),
         "ftp_file_wildcard": get_value(dict, 'File Naming Pattern', None),
         "ftp_file_prefix": get_value(dict, 'FTP File Prefix', ftp_file_prefix(namespace)),
         "namespace": namespace
        }
    )