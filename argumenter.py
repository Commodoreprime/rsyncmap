import argparse
import os

import verbose_printer as vp
from verbose_printer import veprint

__parser = argparse.ArgumentParser(
    prog="rsyncmap",
    description="""
    Rsync wrapper that allows controlling where files and directories should be copied to on a per directory basis
    """)

__parser.add_argument('-v', '--verbose',
            help="toggle output of more information",
            required=False,
            default=False,
            action="store_true",
            dest="verbose")

__parser.add_argument('-o', '--default-options',
            help="options passed to rsync. Defaults to '-hP'",
            required=False,
            default=["-hP"],
            action="store",
            type=list,
            metavar="DEFAULT_OPTIONS",
            dest="def_opts")

__parser.add_argument('-D', '--origin-directory',
            help="directory where to sync from. Defaults to current directory",
            required=False,
            default=None,
            action="store",
            type=str,
            metavar="ORIGIN_DIRECTORY",
            dest="origin_path")

__parser.add_argument('-d', '--dry-run',
            help="executes where nothing is changed, only simulated",
            default=False,
            action="store_true",
            dest="dry_run")

__parser.add_argument("destination_dir",
            help="directory where to sync to",
            type=str)

__args = __parser.parse_args()

verbose:bool = __args.verbose
vp.is_verbose = verbose

dry_run:bool = __args.dry_run

default_flags:list = __args.def_opts
veprint("Default flags = {}".format(default_flags))

if verbose == True:
    default_flags.append("--verbose")
    print("Default flags = {}".format(default_flags))

# If origin_path is None, set to current directory.
#   Otherwise, set to variable
initial_directory:str = None
if __args.origin_path == None:
    initial_directory = os.curdir
elif type(__args.origin_path) == str:
    initial_directory = __args.origin_path
veprint("initial directory = {}".format(initial_directory))

destination_directory:str = __args.destination_dir
veprint("destination directory = {}".format(destination_directory))
