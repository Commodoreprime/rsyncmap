from pathlib import Path
import subprocess

def rsync_executable_path():
    # TODO: Make universal? Does python have a multi-os module for this?
    which_proc = subprocess.run(["which", "rsync"], stdout=subprocess.PIPE)
    if which_proc.returncode == 0:
        return which_proc.stdout.decode().strip()
    return None

def rsync(source_directory:Path, target_directory:Path, arguments:list):
    arg_list = ["rsync"]
    for arg in arguments:
        arg_list.append(arg)
    arg_list.append("--exclude=.syncmap")
    arg_list.append("--info=progress2")
    arg_list.append("--recursive")
    arg_list.append(str(source_directory))
    arg_list.append(str(target_directory))
    target_directory.mkdir(parents=True, exist_ok=True)
    rsync_process = subprocess.run(arg_list)
    return rsync_process
