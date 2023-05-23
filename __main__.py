# Syntax:
# whitespace is ignored unelss quoted
# .             refers to same directory .syncmap file is in
# FROM => TO    the `=>` keyword is used to specify a mapping.
# OR            This is not bidirectional (maybe change to less directional symbol? maybe plain '=').
# if FROM is not specified it will assume same directory as .syncmap
# Therefore, `=> 'New Directory'` is equivilant to: `. => 'New Directory'`
# if TO is not specified it will assume the same directory name as FROM
#   therefore if FROM is also not specified it acts the same as if there was no .syncmap file in the first place (or if it was empty)
#       (a direct mapping from the FROM base directory to the TO base directory)
# if FROM is a file and TO is a directory, unless TO is also a file name, FROM will be placed in the TO directory with the same file name
#   also, if TO is a file and FROM is a directory then TO is written into as if it were a directory
# 
# Glob syntax can be used but only on the left or FROM side
# it is recommended to quote the entire path when specifiying a path with spaces
# like this: ` 'foo/biz/foo and biz go up the hill.txt' => 'story 1.txt' `
#   (though spaces should not prove too much of an issue it may still be good to play it safe)
# If a line starts with a colon (':'), anything after will be considered additional arguments passed to rsync and passed as-is
# If and when declared at some point in the syncmap file it will be added to future mappings for the duration of the file.
from pathlib import PurePath as PuPath

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
            map_pair = line.split("=>")
            if len(map_pair) < 2 and line[0] == ':':
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
                continue
            
            map_from = map_pair[0].strip()
            map_to   = map_pair[1].strip()
        
            mappings_list.append({
                "from": PuPath(syncmap.parent, map_from),
                "to": PuPath(args.destination_directory, map_to),
                "opt_args": opt_arguments
            })

veprint(mappings_list)
# TODO: Delete: Probably don't need this?
# rsync_bin = rsync_executable_path()
# if rsync_bin == None:
#     print("Error! rsync not found!")
#     exit(1)
# veprint("rsync is",rsync_bin)

for mapping in mappings_list:
    rsync_args = args.default_flags
    for ca in mapping["opt_args"]:
        if len(ca) > 0:
            rsync_args.append(ca)
    veprint(' '.join(rsync(str(mapping["from"]), str(mapping["to"]),
        rsync_args)))
