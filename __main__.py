from json import dumps as jdumps
import os

import argumenter as args
from verbose_printer import veprint
from rsync_helper import *
import syncmap

def pprint(obj):
    print(jdumps(obj, indent=2, default=str))

for syncmap_file in syncmap.get_file_list(args.initial_directory):
    parent_directory = os.path.dirname(syncmap_file)
    operation_list = syncmap.parse_file(syncmap_file)
    negation_list:list = []
    arguments_stack:list = []
    arguments_stack.append("--mkpath")
    for i, operation in enumerate(operation_list):
        filter_rules:list = []
        if i == 0: arguments_stack.clear()
        if type(operation) == syncmap.ArgumentsOperator:
            veprint(f"Attemping to modify the arguments stack with these values (removing? {operation.subtractive}): {operation.arguments}")
            if operation.subtractive == False:
                arguments_stack.extend(operation.arguments)
            else:
                for arg in operation.arguments:
                    if arguments_stack.count(arg) > 0:
                        arguments_stack.remove(arg)
        elif type(operation) == syncmap.DirectionOperator:
            source_path:str = parent_directory
            if operation.is_dir == True:
                if (arguments_stack.count("--recursive") + arguments_stack.count("-r")) == 0:
                    arguments_stack.append("--recursive")
                source_path = source_path+'/'
            filter_rules.append(f"--include={operation.from_path}")
            filter_rules.append("--exclude=*")
            rsync(source_path, os.path.join(args.destination_directory, operation.to_path), [args.default_flags, filter_rules, arguments_stack], args.dry_run)
    break
