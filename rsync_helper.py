from pathlib import Path
import subprocess

def rsync_executable_path():
    # TODO: Make universal? Does python have a multi-os module for this?
    which_proc = subprocess.run(["which", "rsync"], stdout=subprocess.PIPE)
    if which_proc.returncode == 0:
        return which_proc.stdout.decode().strip()
    return None

def rsync(source_directory:str, target_directory:str, arguments:list):
    arg_list = ["rsync"]
    for arg in arguments:
        arg_list.append(arg)
    arg_list.append("--dry-run")
    arg_list.append("--info=progress2")
    arg_list.append(source_directory)
    arg_list.append(target_directory)
    return arg_list
    rsync_process = subprocess.run(arg_list, stdout=subprocess.STDOUT)
    return rsync_process
