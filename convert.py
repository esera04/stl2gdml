import pyg4ometry
import pyg4ometry.geant4 as _g4
import xml.etree.ElementTree as ET

reg = _g4.Registry()

materials = {
    "G4_Cu": _g4.MaterialPredefined("G4_Cu", reg),
    "G4_Pb": _g4.MaterialPredefined("G4_Pb", reg),
    "G4_N": _g4.MaterialSingleElement("G4_N", 7, 14.007, 0.00125053, reg),
    "G4_STAINLESS-STEEL": _g4.MaterialPredefined("G4_STAINLESS-STEEL", reg)
}

densities = {
    "G4_Cu": 8.96,
    "G4_Pb": 11.35,
    "G4_N": 0.00125053,
    "G4_STAINLESS-STEEL": 8.02
}

Zs = {
    "G4_Cu": 29,
    "G4_Pb": 82,
    "G4_N": 7,
    "G4_STAINLESS-STEEL": 26
}

As = {
    "G4_Cu": 63.546,
    "G4_Pb": 207.2,
    "G4_N": 14,
    "G4_STAINLESS-STEEL": 55.845
}

symbols = {
    "G4_Cu": 'Cu',
    "G4_Pb": 'Pb',
    "G4_N": 'N',
    "G4_STAINLESS-STEEL": 'Fe'
}

def add_element_to_gdml(root, name, symbol, z, a):
    materials_element = root.find('materials')
    if materials_element is None:
        materials_element = ET.SubElement(root, 'materials')

    if name not in [elm.get('name') for elm in materials_element.findall('element')]:
        element = ET.Element('element', attrib={'name': name, 'formula': symbol, 'Z': str(z)})
        atom = ET.SubElement(element, 'atom', attrib={'value': str(a)})
        materials_element.append(element)
    
    return name

def add_material_to_gdml(root, name, elm_name, density):
    materials_element = root.find('materials')
    if materials_element is None:
        materials_element = ET.SubElement(root, 'materials')

    if name not in [mat.get('name') for mat in materials_element.findall('material')]:
        material = ET.Element('material', attrib={'name': name, 'state': 'solid'})
        density_element = ET.SubElement(material, 'D', attrib={'value': str(density), 'unit': 'g/cm3'})
        fraction = ET.SubElement(material, 'fraction', attrib={'n': '1.0', 'ref': elm_name})
        materials_element.append(material)
    
    return name

print("Available materials:")
for idx, material in enumerate(materials.keys()):
    print(f"{idx}: {material}")

material_choice = int(input("Select a material by number: "))
selected_material_key = list(materials.keys())[material_choice]
selected_material = materials[selected_material_key]

stl_file_path = input("Select source STL file path: ")
reader = pyg4ometry.stl.Reader(stl_file_path)
gdml_file_path = ".".join(stl_file_path.split(".")[:-1] + ["gdml"])
reader.writeDefaultGDML(gdml_file_path)

tree = ET.parse(gdml_file_path)
root = tree.getroot()
materials_element = root.find('materials')
elm_name = add_element_to_gdml(root, 'ELM_' + selected_material_key, symbols[selected_material_key], Zs[selected_material_key], As[selected_material_key])

if materials_element is None:
    materials_element = ET.SubElement(root, 'materials')

if selected_material_key not in [mat.get('name') for mat in materials_element.findall('material')]:
    material_element = ET.Element('material', attrib={'name': selected_material_key})
    
    density_value = str(densities[selected_material_key])
    density = ET.SubElement(material_element, 'D', attrib={'value': density_value, 'unit': 'g/cm3'})
    fraction = ET.SubElement(material_element, 'fraction', attrib={'n': '1.0', 'ref': elm_name})

    if hasattr(selected_material, 'components'):
        for component in selected_material.components:
            composite = ET.SubElement(material_element, 'composite', attrib={'n': str(component[1]), 'ref': component[0]})
    
    materials_element.append(material_element)
material_name = add_material_to_gdml(root, selected_material_key, elm_name, densities[selected_material_key])

solids_element = root.find('solids')
for solid in solids_element:
    solid.set('materialref', material_name)

structure_element = root.find('structure')
for volume in structure_element.findall('volume'):
    volume_material_ref = volume.find('materialref')
    if volume_material_ref is None:
        material_ref = ET.SubElement(volume, 'materialref', attrib={'ref': material_name})
    else:
        volume_material_ref.set('ref', material_name)

tree.write(gdml_file_path)