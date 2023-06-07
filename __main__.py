from pathlib import Path

import argumenter as args
from verbose_printer import veprint
from rsync_helper import *
import syncmap


mapping_files = args.initial_directory.glob("**/.syncmap")
mappings_list = []

for syncmap_file in mapping_files:
    mappings_list += syncmap.parse_file(syncmap_file)

def generate_exclude(input_entry:syncmap.DirectionOperator|syncmap.NegationOperator):
    _type = type(input_entry)
    if _type == syncmap.DirectionOperator:
        return f"--exclude={input_entry.from_path}"
    elif _type == syncmap.NegationOperator:
        return f"--exclude={input_entry.negator}"

exclude_list = []
#TODO?: Change so that it does not appear in *every* command
universal_exclude_list = []
for mapping in mappings_list:
    entry_type = type(mapping["operation"])
    operation = mapping["operation"]
    
    new_exclude = generate_exclude(operation)
    if entry_type == syncmap.NegationOperator:
        universal_exclude_list.append(new_exclude)
    exclude_list.append(new_exclude)

mappings_list.insert(0, {
    "operation": syncmap.DirectionOperator(Path(args.initial_directory,'*'),
                                           args.destination_directory),
    "opt_args": exclude_list
})

for mapping in mappings_list:
    if mapping["opt_args"] == None:
        continue
    rsync_args = args.default_flags + mapping["opt_args"] + universal_exclude_list
    operation = mapping["operation"]
    rsync(operation.from_path, operation.to_path, rsync_args)
