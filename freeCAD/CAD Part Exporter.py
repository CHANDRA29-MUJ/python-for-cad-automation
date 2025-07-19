import FreeCAD as App
import Part
import Import
import Mesh
import csv
import os
import math

# Input File Paths - Not Complete So Please Fill According to Your Needs - Without this input, Code Will Not Work
input_csv = r"C:\\input_parts.csv"
output_dir = r"C:\\generated_parts"
bom_file = "BOM.csv"

App.newDocument("BOM_Generator")
doc = App.ActiveDocument

try:
    os.makedirs(output_dir, exist_ok=True)
except PermissionError as e:
    print(f"Could not create folder: {output_dir}")
    print(e)
    App.closeDocument(doc.Name)
    raise

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# Geometry functions
def make_washer(id, od, thickness):
    return Part.makeCylinder(od/2, thickness).cut(Part.makeCylinder(id/2, thickness))

def make_spacer(id, od, thickness):
    return make_washer(id, od, thickness)

def make_flange(id, od, thickness, lip_od, lip_thickness, hole_dia=5, num_holes=4, pcd=None):
    base = Part.makeCylinder(od/2, thickness)
    hole = Part.makeCylinder(id/2, thickness + lip_thickness)
    lip = Part.makeCylinder(lip_od/2, lip_thickness)
    lip.translate(App.Vector(0, 0, thickness))
    flange = base.fuse(lip).cut(hole)

    if not pcd:
        pcd = (od + id) / 2  # Default pitch circle diameter

    hole_radius = hole_dia / 2
    angle_step = 360 / num_holes

    for i in range(num_holes):
        angle = math.radians(i * angle_step)
        x = (pcd / 2) * math.cos(angle)
        y = (pcd / 2) * math.sin(angle)
        bolt_hole = Part.makeCylinder(hole_radius, thickness + lip_thickness)
        bolt_hole.translate(App.Vector(x, y, 0))
        flange = flange.cut(bolt_hole)

    return flange

# BOM Creation
bom_data = []

with open(input_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        part_type = row['type'].lower()
        id = safe_float(row.get('id'))
        od = safe_float(row.get('od'))
        thickness = safe_float(row.get('thickness'))
        quantity = safe_int(row.get('quantity', 1))

        lip_od = safe_float(row.get('lip_od'))
        lip_thickness = safe_float(row.get('lip_thickness'))

        hole_dia = safe_float(row.get('hole_dia', 5))
        num_holes = safe_int(row.get('num_holes', 4))
        pcd = safe_float(row.get('pcd', 0)) or None

       
        if od <= 0 or id < 0 or thickness <= 0 or id >= od:
            print(f"Skipping invalid {part_type}: ID={id}, OD={od}, Thickness={thickness}")
            continue
        if part_type == 'flange' and (lip_od <= od or lip_thickness <= 0):
            print(f"Invalid flange lip dimensions for OD={od}, Lip_OD={lip_od}")
            continue

        part_name = f"{part_type}_{int(od)}x{int(id)}x{int(thickness)}"

     
        if part_type == 'washer':
            shape = make_washer(id, od, thickness)
        elif part_type == 'spacer':
            shape = make_spacer(id, od, thickness)
        elif part_type == 'flange':
            shape = make_flange(id, od, thickness, lip_od, lip_thickness, hole_dia, num_holes, pcd)
        else:
            print(f"Unknown part type: {part_type}")
            continue

        
        part_obj = doc.addObject("Part::Feature", part_name)
        part_obj.Shape = shape
        App.ActiveDocument.recompute()

        path = os.path.join(output_dir, part_name)
        part_obj.Shape.exportStep(path + ".step")
        Mesh.export([part_obj], path + ".stl")
        Import.export([part_obj], path + ".fcstd")

      
        bom_data.append({
            'Name': part_name,
            'Type': part_type,
            'ID (mm)': id,
            'OD (mm)': od,
            'Thickness (mm)': thickness,
            'Lip OD (mm)': lip_od if part_type == 'flange' else '',
            'Lip Thickness (mm)': lip_thickness if part_type == 'flange' else '',
            'Hole Dia (mm)': hole_dia if part_type == 'flange' else '',
            'Num Holes': num_holes if part_type == 'flange' else '',
            'PCD (mm)': pcd if part_type == 'flange' else '',
            'Quantity': quantity
        })

bom_fields = ['Name', 'Type', 'ID (mm)', 'OD (mm)', 'Thickness (mm)',
              'Lip OD (mm)', 'Lip Thickness (mm)',
              'Hole Dia (mm)', 'Num Holes', 'PCD (mm)', 'Quantity']

with open(os.path.join(output_dir, bom_file), 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=bom_fields)
    writer.writeheader()
    writer.writerows(bom_data)

print("Done: Parts generated, bolt-hole flanges included, and BOM exported.")
