import subprocess
import os

def rsync_executable_path():
    # TODO: Make universal? Does python have a multi-os module for this?
    which_proc = subprocess.run(["which", "rsync"], stdout=subprocess.PIPE)
    if which_proc.returncode == 0:
        return which_proc.stdout.decode().strip()
    return None

#TODO: Add option that allows user to block adding internal args
def rsync(source_directory:str, target_directory:str, arguments:[list],
          fake:bool=False) -> subprocess.CompletedProcess[bytes]|None:
    arg_list = ["rsync"]
    for a_list in arguments:
        if type(a_list) == list:
            arg_list.extend(a_list)
        else:
            arg_list.append(a_list)
    arg_list.append(source_directory)
    arg_list.append(target_directory)
    print(' '.join(arg_list))
    if fake == False:
        rsync_process = subprocess.run(arg_list)
        return rsync_process
    return None
