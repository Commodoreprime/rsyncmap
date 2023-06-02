import sys

is_verbose = False

def veprint(*output_text, error:bool=False) -> None:
    if is_verbose == False: return
    output_pipe = sys.stdout
    if error == True:
        output_pipe = sys.stderr
    print(*output_text, file=output_pipe)
