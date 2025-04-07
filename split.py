import FreeCAD
import Part
import Mesh
import os

# export PYTHONPATH=/usr/lib/freecad/lib:$PYTHONPATH
# run above before running this

step_file = "TPC Shrinked.STEP"
whole_stl_file = "whole_model.stl"
output_dir = "split_components"

if not os.path.isfile(step_file):
    raise FileNotFoundError(f"File not found: {step_file}")

os.makedirs(output_dir, exist_ok=True)

doc = FreeCAD.newDocument("WholeModel")
shape = Part.read(step_file)
compound_obj = doc.addObject("Part::Feature", "WholeModel")
compound_obj.Shape = shape

Mesh.export([compound_obj], whole_stl_file)
print(f"Exported {whole_stl_file}")

mesh = Mesh.Mesh(whole_stl_file)

components = mesh.getSeparateComponents()  

for i, component in enumerate(components, start=1):
    component_file = os.path.join(output_dir, f"Component_{i}.stl")
    component.write(component_file)
    print(f"Exported Component_{i} to {component_file}")

print("All components exported successfully!")
