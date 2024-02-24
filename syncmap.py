import pathlib as pl
import os

class GenericOperator:
    def __init__(self):
        self.exclude:str = None
        self.include:str = None
        self.order_index:int = 0

class DirectionOperator(GenericOperator):
    def __init__(self, _from_target:str, _to:str, _idx:int, _parent:str=""):
        super().__init__()
        self.from_path:str = os.path.join(_parent, _from_target)
        self.to_path:str = _to
        self.from_target:str = _from_target.strip()
        self.from_parent:str = _parent.strip()
        self.is_globbed:bool = (_from_target.count('*') > 0) or (_from_target.count('\*') != _from_target.count('*'))
        self.is_dir:bool = os.path.isdir(os.path.join(os.environ["PWD"], self.from_path)) or \
                           (os.path.isdir(os.path.join(os.environ["PWD"], self.from_parent)) and self.is_globbed)
        self.order_index:int = _idx
        
        self.exclude = f"-f- /{self.from_target}"
        self.include = f"-f+ /{self.from_target}"

    def __str__(self) -> str:
        return f"DIRECT ({self.order_index}) from({self.from_path}), to({self.to_path}), is_dir({self.is_dir}), is_globbed({self.is_globbed})"

class NegationOperator(GenericOperator):
    def __init__(self, _negator_target:str, _idx:int, _parent:str=""):
        super().__init__()
        self.parent_path:str = _parent
        self.negator:str = _negator_target.strip()
        self.full_path:str = os.path.join(_parent, _negator_target)
        self.order_index:int = _idx
        
        self.exclude = f"-f- /{self.negator}"
        self.include = f"-f+ /{self.negator}"
    
    def __str__(self) -> str:
        return f"NEGATE ({self.order_index}) {self.negator}"

class ArgumentsOperator():
    def __init__(self, _list_of_args:list, _idx:int, _subtractive:bool=False):
        self.arguments:list = _list_of_args
        self.subtractive:bool = _subtractive
        self.order_index:int = _idx
    
    def __str__(self) -> str:
        return f"ARGS ({self.order_index}) {self.arguments}, remove?({self.subtractive})"

def get_file_list(start_directory:str) -> list:
    return pl.Path(start_directory).rglob(".syncmap")

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
    return arg_list

def clean_comments(input_line:str) -> str:
    first_index = input_line.find('#')
    if first_index == -1:
        return input_line
    return input_line[:first_index]

def parse_file(file_path:str) -> list:
    """Transform plaintext file from file_path into a list of operators
    """
    operation_return_list: list = []
    with open(file_path, 'r') as f:
        for i, raw_line in enumerate(f.readlines()):
            line = clean_comments(raw_line)
            if len(line) == 0: continue
            if line.startswith(":"):
                new_arguments = extract_arguments(line)
                operation_return_list.append(ArgumentsOperator(new_arguments[1:], i, line.startswith(":- ")))
                continue
            elif line[0] == '!':
                operation_return_list.append(NegationOperator(line[1:], i))
                continue
            # If all previous conditions don't meet, we assume the operation is a redirection operator
            direction_operation_args = extract_arguments(line)
            if direction_operation_args[0] == '.':
                direction_operation_args[0] = ""
            if direction_operation_args[1] != "=>": continue
            operation_return_list.append(DirectionOperator(direction_operation_args[0], direction_operation_args[2], i))
    return operation_return_list
