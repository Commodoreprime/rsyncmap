import sys

is_verbose = False

def veprint(*output_text, error:bool=False) -> None:
    output_pipe = sys.stdout
    if error == True:
        output_pipe = sys.stderr
    if is_verbose:
        print(*output_text, file=output_pipe)
