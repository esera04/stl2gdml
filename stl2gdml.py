#!/usr/bin/python3

import os
import argparse

from contextlib import contextmanager, redirect_stderr, redirect_stdout

@contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

def main(args):
    filename = args["filename"]
    verbose = args["verbose"]
    to = args["to"]
    display = args["display"]

    if not verbose:
        with suppress_stdout_stderr():
            import pyg4ometry
    else:
        import pyg4ometry

    reader = pyg4ometry.stl.Reader(filename)
    reader.writeDefaultGDML(to)

    print(f"Wrote output GDML to {to}")

    if display:
        print("Activating display...")
        output_gdml = pyg4ometry.gdml.Reader(to)
        v = pyg4ometry.visualisation.VtkViewer()
        v.addLogicalVolume(output_gdml.getRegistry().getWorldVolume())
        v.view()

    print("Terminating...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="stl2gdml", description="Command line tool to convert STL to GDML")
    parser.add_argument("filename", help="source STL file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display warnings and errors")
    parser.add_argument("-t", "--to", help="Destination GDML file name", default="output.gdml")
    parser.add_argument("-d", "--display", action="store_true", help="Visualize output volume using OpenGL")
    args = parser.parse_args()

    main(vars(args))
