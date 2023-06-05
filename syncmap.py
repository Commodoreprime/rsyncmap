from pathlib import Path

import argumenter as args

def extract_arguments(input_line:str) -> list:
    """Given an line str. extract a list of arguments while accounting for quotes"""
    arg_list = []
    buffer = ""
    quote_level = 0
    for c in input_line:
        if c == ' ' and quote_level == 0:
            arg_list.append(buffer)
            buffer = ''
        else:
            buffer += c
        if c == '"' or c == "'":
            quote_level += 1
            if quote_level >= 1:
                quote_level -= 2
    return arg_list

def parse_file(file_path:Path) -> list:
    transform_list = []
    with file_path.open('r') as f:
        additional_arguments = []
        for line in f.readlines():
            if line.startswith(':'):
                additional_arguments += extract_arguments(line[1:].strip()+' ')
            elif line.startswith('!'):
                transform_list.append({
                    "negate": Path(file_path.parent, line[1:].strip())
                })
            else:
                pair = line.split("=>")
                from_path = Path(file_path.parent, pair[0].strip())
                to_path = Path(args.destination_directory, pair[1].strip())
                transform_list.append({
                    "opt_args": additional_arguments.copy(),
                    "from": from_path,
                    "to": to_path
                })
    return transform_list
