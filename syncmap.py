import glob
import os

import argumenter as args

class GenericOperator:
    def __init__(self):
        self.exclude:str = None
        self.include:str = None

class DirectionOperator(GenericOperator):
    def __init__(self, _parent:str, _from_target:str, _to:str):
        super().__init__()
        self.from_path:str = os.path.join(_parent, _from_target)
        self.to_path:str = _to
        self.from_target:str = _from_target
        self.from_parent:str = _parent
        self.is_globbed:bool = (_from_target.count('*') > 0) or (_from_target.count('\*') != _from_target.count('*'))
        self.is_dir:bool = os.path.isdir(self.from_path) #_from_target.endswith('/')
        
        self.exclude = f"-f- /{self.from_target}"
        self.include = f"-f+ /{self.from_target}"

    def __str__(self) -> str:
        return f"DIRECT from({self.from_path}), to({self.to_path}), is_dir({self.is_dir}), is_globbed({self.is_globbed})"

class NegationOperator(GenericOperator):
    def __init__(self, _parent:str, _negator_target:str):
        super().__init__()
        self.parent_path:str = _parent
        self.negator:str = _negator_target
        self.full_path:str = os.path.join(_parent, _negator_target)
        
        self.exclude = f"-f- /{self.negator}"
        self.include = f"-f+ /{self.negator}"
    
    def __str__(self) -> str:
        return f"NEGATE {self.negator}, full_path({self.full_path})"

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

def clean_comments(input_line:str) -> str:
    first_index = input_line.find('#')
    if first_index == -1:
        return input_line
    return input_line[:first_index]

def parse_file(file_path:str) -> list:
    transform_list = []
    def add_entry(map:DirectionOperator|NegationOperator, args:list|None, push_top:bool=False):
        if type(args) == list:
            args = args.copy()
        new_entry = {
            "operation": map,
            "opt_args": args
        }
        if push_top == True:
            transform_list.insert(0, new_entry)
        else:
            transform_list.append(new_entry)
    arguments_buffer = []
    with open(file_path, 'r') as f:
        parent_directory = os.path.dirname(file_path)
        for rawline in f.readlines():
            line = clean_comments(rawline).strip()
            pair = line.split("=>")
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
                target = line[1:].strip()
                add_entry(NegationOperator(parent_directory, target), None, push_top=True)
            elif len(pair) > 1:
                from_entry = pair[0].strip()
                if from_entry == ('' or '.'):
                    from_entry = '*'
                to_path = os.path.join(args.destination_directory, pair[1].strip())
                add_entry(DirectionOperator(parent_directory, from_entry, to_path),
                          arguments_buffer)
    return transform_list
