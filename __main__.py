from pathlib import Path

from argumenter import Argumenter
from verbose_printer import veprint
from rsync_helper import *


args = Argumenter()

mapping_files = args.initial_directory.glob("**/.syncmap")
mappings_list = []

for syncmap in mapping_files:
    with syncmap.open('r') as f:
        opt_arguments = []
        for line in f.readlines():
            if line[0] == ':':
                buffer = ''
                quote_level = 0
                for c in line[1:].strip() + ' ':
                    if c == ' ' and quote_level == 0:
                        opt_arguments.append(buffer)
                        buffer = ''
                    else:
                        buffer += c
                    if c == '"' or c == "'":
                        quote_level += 1
                        if quote_level >= 1:
                            quote_level -= 2
            else:
                map_pair = line.split("=>")
                map_from = Path(syncmap.parent, map_pair[0].strip())
                map_to   = Path(args.destination_directory, map_pair[1].strip())
                mappings_list.append({
                    "from": map_from,
                    "to": map_to,
                    "opt_args": opt_arguments.copy()
                })

veprint(mappings_list)

for mapping in mappings_list:
    rsync_args = args.default_flags + mapping["opt_args"]
    veprint(rsync(str(mapping["from"]), str(mapping["to"]), rsync_args))
