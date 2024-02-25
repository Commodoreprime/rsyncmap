
def extract_arguments(input_line:str) -> list:
    """Given an line str. extract a list of arguments while accounting for quotes"""
    arg_list = []
    buffer = ""
    quote_level = 0
    for i, c in enumerate(input_line):
        if (c == ' ' and quote_level == 0) or i == len(input_line) - 1:
            arg_list.append(buffer)
            buffer = ''
        else:
            buffer += c
        if (c == '"' or c == '\'') and input_line[i-1] != '\\':
            quote_level += 1
            if quote_level >= 1:
                quote_level -= 2
    # When the list returns, arguments that contain intentional whitespacespace ("like this"),
    #   results in the list element also including the quoting chars, TODO: Fix this.
    #   ( this should only happen if the user is specifically escaping the chars (\", \') )
    return arg_list
