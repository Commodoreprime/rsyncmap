from pathlib import Path

import argumenter as args
from verbose_printer import veprint
from rsync_helper import *
import syncmap


mapping_files = args.initial_directory.glob("**/.syncmap")
mappings_list = []

for syncmap_file in mapping_files:
    mappings_list += syncmap.parse_file(syncmap_file)

veprint(mappings_list)

for mapping in mappings_list:
    rsync_args = args.default_flags + mapping["opt_args"]
    rsync(mapping["from"], mapping["to"], rsync_args)
