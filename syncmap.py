import glob
import os

import argumenter as args

class DirectionOperator:
    def __init__(self, _from:str, _to:str):
        self.from_path:str = _from
        self.to_path:str = _to

    def __str__(self) -> str:
        return f"{self.from_path} -> {self.to_path}"

class NegationOperator:
    def __init__(self, _negator_path:str):
        self.negator:str = _negator_path
    
    def __str__(self) -> str:
        return f"! {self.negator}"

def get_file_list(start_directory:str) -> list:
    glob_list = glob.glob("**/.syncmap", root_dir=start_directory, recursive=True)
    return_list = []
    for glob_file in glob_list:
        return_list.append(os.path.join(start_directory, glob_file))
    return return_list

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

def parse_file(file_path:str) -> list:
    transform_list = []
    def add_entry(map:DirectionOperator|NegationOperator, args:list|None):
        if type(args) == list:
            args = args.copy()
        transform_list.append({
            "operation": map,
            "opt_args": args
        })
    arguments_buffer = []
    with open(file_path, 'r') as f:
        parent_directory = os.path.dirname(file_path)
        for line in f.readlines():
            if line.startswith(':'):
                remove_args = False
                argument_str = line[1:].strip()
                if argument_str.startswith('- '):
                    argument_str = line[1:].strip()
                    remove_args = True
                for arg in extract_arguments(argument_str+' '):
                    if remove_args == False:
                        arguments_buffer.append(arg)
                    elif remove_args == True:
                        try:
                            arguments_buffer.remove(arg)
                        except ValueError: pass
            elif line.startswith('!'):
                add_entry(NegationOperator(os.path.join(parent_directory,
                                                        line[1:].strip())),
                          None)
            else:
                pair = line.split("=>")
                from_entry = pair[0].strip()
                if from_entry == ('' or '.'):
                    from_entry = '*'
                to_path = os.path.join(args.destination_directory, pair[1].strip())
                for deg_file in glob.glob(from_entry, root_dir=parent_directory):
                    add_entry(DirectionOperator(os.path.join(parent_directory, deg_file), to_path),
                              arguments_buffer)
    return transform_list
