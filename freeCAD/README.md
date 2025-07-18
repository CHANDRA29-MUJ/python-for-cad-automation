# FreeCAD Part Generator – Washers, Spacers, Flanges (with BOM Export)

This Python script automates the creation of **washer**, **spacer**, and **flange** models using **FreeCAD**, based on parameters from a CSV file. It exports the parts in `.STEP`, `.STL`, and also generates a **Bill of Materials (BOM)** as a CSV.

---

## Features

- Parametric 3D part generation (washers, spacers, flanges with bolt holes)
- CSV-driven automation
- Outputs:
  - `.STEP` – CAD exchange format
  - `.STL` – For 3D printing
  - `BOM.csv` – Summary of all generated parts

---

## 📁 Input Paths (Modify Before Running)

The input file must be a CSV file and the output must be a folder. 
Before running the script, **update the paths** in the “Input File Paths” section:

```python
input_csv = r"Path\To\Your\Input\input_parts.csv"
output_dir = r"Path\To\Your\Output\Folder"

