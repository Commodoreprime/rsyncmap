from sys import argv
from pprint import pprint
import os

from rsync_helper import *
from utils import *

argvlen = len(argv)
source_directory = argv[argvlen - 2]
target_directory = argv[argvlen - 1]
additional_args = argv[1:argvlen - 2]

if os.path.isdir(source_directory) == False or os.path.isdir(target_directory) == False:
    print("Need at least a valid source and destination directory!")
    exit(1)

dry_run:bool = (argv.count("--dry-run") + argv.count("-n")) > 0
verbose:bool = (argv.count("--verbose") + argv.count("-v")) > 0

if verbose: print(f"source: {source_directory} dest: {target_directory} additional args: {additional_args}")

root_syncmap = os.path.join(source_directory, ".syncmap")

syncmap_abstract = {}

if os.path.isfile(root_syncmap) == False:
    print(".syncmap files does not exist!")
    exit(1)

with open(root_syncmap) as f:
    last_idx = None
    for i, line in enumerate(f.readlines()):
        argus = extract_arguments(line)
        if len(line.strip()) == 0: continue
        if argus[1] == "=>":
            syncmap_abstract.update({
                i: {
                    "from": argus[0],
                    "to": argus[2],
                    "filter_rules": [],
                }
            })
            last_idx = i
            continue
        if last_idx == None:
            syncmap_abstract.update({
                0: {
                    "from": "",
                    "to": "",
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
    rsync(os.path.join(source_directory, entry["from"]), os.path.join(target_directory, entry["to"]), [additional_args, filter_args], dry_run)

exit(0)
