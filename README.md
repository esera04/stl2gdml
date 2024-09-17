# stl2gdml

## Prerequisites

Make sure to have installed Python3.8+. To install necessary Python packages, run `pip install -r requirements.txt`.

## Conversion without Materials
View usage and help messages using `python3 stl2gdml.py --help`. 

Example usage:
```bash
python3 stl2gdml.py twins.stl --to twins.gdml --display
```
This will convert `twins.stl` to `twins.gdml` and display the result with OpenGL.

## Conversion with Materials
ElementTree XML editor generates correct materials tag with references within the structure based on predefined elements in Geant4. Requires manual addition of atomic mass, number, and density for each material defined. 
```
$ python3 convert.py 

Available materials:
0: G4_Cu
1: G4_Pb
2: G4_N
3: G4_STAINLESS-STEEL
Select a material by number: 3
Select source STL file path: examples/arms.stl
```
Will output result to `examples/arms.gdml`.

## Author
Edward Serafimescu (eserafimescu@ucla.edu)


## Citation
S.D. Walker, A. Abramov, L.J. Nevay, W. Shields, S.T. Boogert, pyg4ometry: A Python library for the creation of Monte Carlo radiation transport physical geometries, Computer Physics Communications 272 108228 (2022).