def clean_comma_delimited_string(string):
    """
    Takes a comma-delimited string and makes sure it contains
    only unique values and begins and ends with commas.  If string
    is None return empty string
    """

    if string == None:
        return ''

    tmp = [ str(val) + ',' for val in sorted(set(string.split(','))) if val ]
    return ',' + ''.join(tmp)
