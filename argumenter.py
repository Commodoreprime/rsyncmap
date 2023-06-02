from pathlib import Path
import argparse
import os

import verbose_printer as vp
from verbose_printer import veprint

class Argumenter:
    def __init__(self, premature_stop=False) -> None:
        self.parser = argparse.ArgumentParser(
            prog="rsyncmap",
            description="""
            Rsync wrapper that allows controlling where files and directories should be copied to on a per directory basis
            """)
        
        # Defines arguments
        self.parser.add_argument('-v', '--verbose',
            help="toggle output of more information",
            required=False,
                                default=False,
                                action="store_true",
                                dest="_verbose")
        self.parser.add_argument('-o', '--default-options',
            help="options passed to rsync. Defaults to '-hP'",
            required=False,
                                default=["-hP"],
                                action="store",
                                type=list,
                                metavar="DEFAULT_OPTIONS",
                                dest="_def_opts")
        self.parser.add_argument('-D', '--origin-directory',
            help="directory where to sync from. Defaults to current directory",
            required=False,
                                default=None,
                                action="store",
                                type=Path,
                                metavar="ORIGIN_DIRECTORY",
                                dest="_origin_path")
        self.parser.add_argument('-d', '--dry-run',
            help="executes where nothing is changed, only simulated",
                                default=False,
                                action="store_true",
                                dest="_dry_run")
        self.parser.add_argument("destination_dir",
            help="directory where to sync to",
                                type=Path)
        
        # Parse arguments and store into variables
        self.args = self.parser.parse_args()
        
        self.verbose:bool = self.args._verbose
        vp.is_verbose = self.verbose
        
        self.dry_run:bool = self.args._dry_run
        
        self.default_flags:list = self.args._def_opts
        veprint("Default flags = {}".format(self.default_flags))
        
        if self.verbose == True:
            self.default_flags.append("--verbose")
            print("Default flags = {}".format(self.default_flags))
        
        # If origin_path is None, set to current directory.
        #   Otherwise, set to variable
        self.initial_directory:Path = Path()
        if self.args._origin_path == None:
            self.initial_directory = Path(os.curdir)
        elif self.args._origin_path is Path:
            self.initial_directory = self.args._origin_path
        veprint("initial directory = {}".format(self.initial_directory))
        
        self.destination_directory:Path = self.args.destination_dir
        veprint("destination directory = {}".format(self.destination_directory))
