from json import dumps as jdumps
import os

import argumenter as args
from verbose_printer import veprint
from rsync_helper import *
import syncmap

def pprint(obj):
    print(jdumps(obj, indent=2, default=str))

syncmaps:dict = {}
for syncmap_file in sorted(syncmap.get_file_list(args.initial_directory), reverse=True):
    print(syncmap_file)
    syncmaps[os.path.dirname(syncmap_file)] = syncmap.parse_file(syncmap_file)

pprint(syncmaps)

for map_key in syncmaps:
    operation_list = syncmaps[map_key]
    negation_list:list = []
    for map_item in operation_list:
        operation:syncmap.GenericOperator = map_item["operation"]
        if type(operation) == syncmap.NegationOperator:
            negation_list.append(operation.exclude)
        elif type(operation) == syncmap.DirectionOperator:
            source_path:str = map_key
            additonal_filters = []
            if operation.is_dir == True:
                source_path = os.path.join(source_path, operation.from_target)
                for negation in negation_list:
                    additonal_filters.append(negation.replace(operation.from_target, ''))
            elif operation.is_globbed == False:
                source_path = os.path.join(source_path, operation.from_target)
            if operation.is_globbed == True:
                dir_glob_pair:list = operation.from_target.rsplit('/', maxsplit=1)
                source_path = os.path.join(source_path, dir_glob_pair[0]+'/')
                additonal_filters.append("-m")
                additonal_filters.append("-f+ */")
                additonal_filters.append(f"-f+ {dir_glob_pair[1]}")
                additonal_filters.append("-f- *")
            rsync(source_path, operation.to_path, [ args.default_flags,
                                                    map_item["opt_args"],
                                                    additonal_filters ], args.dry_run)
