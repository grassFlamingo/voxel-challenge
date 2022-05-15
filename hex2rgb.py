import argparse

_arg = argparse.ArgumentParser()
_arg.add_argument("color", type=str)
args = _arg.parse_args()

def hex2rgb(x: str):
    #
    x = x.strip("#")

    r = int(f"0x{x[0:2]}", base=16) 
    g = int(f"0x{x[2:4]}", base=16) 
    b = int(f"0x{x[4:6]}", base=16) 

    return f"vec3({r/255 :.2f}, {g/255 :.2f}, {b/255:.2f})"


print(args.color, hex2rgb(args.color))
