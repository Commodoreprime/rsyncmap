from pathlib import Path

import argumenter as args

class DirectionOperator:
    def __init__(self, _from:Path|str, _to:Path|str):
        self.from_path:Path = Path(_from)
        self.to_path:Path = Path(_to)

    def __str__(self) -> str:
        return f"{self.from_path} -> {self.to_path}"

class NegationOperator:
    def __init__(self, _negator_path:Path|str):
        self.negator:Path = Path(_negator_path)
    
    def __str__(self) -> str:
        return f"! {self.negator}"

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
    def add_entry(map:DirectionOperator|NegationOperator, args:list|None):
        if type(args) == list:
            args = args.copy()
        transform_list.append({
            "operation": map,
            "opt_args": args
        })
    arguments_buffer = []
    with file_path.open('r') as f:
        for line in f.readlines():
            if line.startswith(':'):
                remove_args = False
                argument_str = line[1:].strip()
                if argument_str.startswith('- '):
                    argument_str = line[2:]
                    remove_args = True
                for arg in extract_arguments(argument_str+' '):
                    if remove_args == False:
                        arguments_buffer.append(arg)
                    elif remove_args == True:
                        try:
                            arguments_buffer.remove(arg)
                        except ValueError: pass
            elif line.startswith('!'):
                add_entry(NegationOperator(Path(file_path.parent, line[1:].strip())),
                          None)
            else:
                pair = line.split("=>")
                from_entry = pair[0].strip()
                if from_entry == '':
                    from_entry = '*'
                to_path = Path(args.destination_directory, pair[1].strip())
                for deglobbed_path in file_path.parent.glob(from_entry):
                    add_entry(DirectionOperator(deglobbed_path, to_path),
                              arguments_buffer)
    return transform_list
