import pathlib as pl
from sys import argv
from pprint import pprint
import os

from rsync_helper import *
from utils import *

argvlen = len(argv)
source_directory = pl.Path(argv[argvlen - 2])
target_directory = pl.Path(argv[argvlen - 1])
additional_args = argv[1:argvlen - 2]

dry_run:bool = (argv.count("--dry-run") + argv.count("-n")) > 0
verbose:bool = (argv.count("--verbose") + argv.count("-v")) > 0

if verbose: print(f"source: {source_directory} dest: {target_directory} additional args: {additional_args}")

root_syncmap = source_directory.joinpath(".syncmap")

syncmap_abstract = {}

if root_syncmap.exists() == False:
    print(".syncmap files does not exist!")
    exit(1)

with open(root_syncmap) as f:
    last_idx = None
    for i, line in enumerate(f.readlines()):
        argus = extract_arguments(line)
        if argus[1] == "=>":
            syncmap_abstract.update({
                i: {
                    "from": (argus[0], argus[0].endswith(os.sep)),
                    "to": (argus[2], argus[2].endswith(os.sep)),
                    "filter_rules": [],
                }
            })
            last_idx = i
            continue
        if last_idx == None:
            syncmap_abstract.update({
                0: {
                    "from": ("", True),
                    "to": ("", False),
                    "filter_rules": []
                }
            })
            last_idx = 0
        syncmap_abstract[last_idx]["filter_rules"].append(line.strip())

if verbose: pprint(syncmap_abstract, indent=2)

for i in syncmap_abstract.keys():
    entry = syncmap_abstract[i]
    filter_args = []
    if len(entry["filter_rules"]) > 0:
        for filter in entry["filter_rules"]:
            filter_args.append(f"--filter={filter}")
    final_source_path = str(source_directory.joinpath(entry["from"][0]))
    final_dest_path = str(target_directory.joinpath(entry["to"][0]))
    if entry["from"][1] == True:
        final_source_path = f"{final_source_path}{os.sep}"
    if entry["to"][1] == True:
        final_dest_path = f"{final_dest_path}{os.sep}"
    rsync(final_source_path, final_dest_path, [additional_args, filter_args], dry_run)

exit(0)
