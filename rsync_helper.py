import subprocess
import os

def rsync_executable_path():
    # TODO: Make universal? Does python have a multi-os module for this?
    which_proc = subprocess.run(["which", "rsync"], stdout=subprocess.PIPE)
    if which_proc.returncode == 0:
        return which_proc.stdout.decode().strip()
    return None

def rsync(source_directory:str, target_directory:str, arguments:list,
          fake:bool=False) -> subprocess.CompletedProcess[bytes]|None:
    arg_list = ["rsync"]
    arg_list.append("--exclude=.syncmap")
    arg_list += arguments
    arg_list.append(source_directory)
    arg_list.append(target_directory)
    print(' '.join(arg_list))
    if fake == False:
        os.makedirs(target_directory, exist_ok=True)
        rsync_process = subprocess.run(arg_list)
        return rsync_process
    return None
