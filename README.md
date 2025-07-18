# 🛠️ Python for CAD Automation

This is a personal toolkit of Python scripts designed to automate 3D part generation and export using popular CAD platforms like **FreeCAD** and **Fusion 360**. The goal is to streamline repetitive modeling tasks and enable parametric design through simple CSV or user input.

📌 Why This Project?
As a mechanical engineering student, I wanted to reduce time spent on repetitive modeling by building my own Python-based CAD automation tools. This repo serves as a learning playground and a growing toolkit for design automation.

---

## 🚀 What’s Included

### 📌 FreeCAD Tools
- **Washer/Spacer/Flange Generator**
  - Reads part parameters from a CSV file
  - Creates 3D models of washers, spacers, and flanges
  - Adds bolt holes and lips for flanges
  - Exports to `.STEP` and `.STL`
  - Generates a complete `BOM.csv`


---

### ⚙️ Fusion 360 Add-ins 
- **Bolt Generator**
- **Gear Generator**

These are custom Python scripts built using Fusion 360’s API, designed for generating fasteners and gear profiles parametrically.

---

## 📂 Project Structure
- FreeCAD Folder
- Fusion 360 Folder

Contain all the relevant files 


---

## 💡 How to Use

### ✅ FreeCAD Scripts
1. Open FreeCAD.
2. Go to: `Utilities > Add-ins > Macros`
3. Create a new macro and paste the script 
4. Update the `input_csv` and `output_dir` paths inside the script.
5. Run the macro.
6. Parts will be exported and BOM generated in the specified folder.

### ✅ Fusion 360 Add-ins
1. Open Fusion 360.
2. Go to: `Tools > Scripts and Add-ins`
3. Copy the script in the a newly created Script (Python)
4. Run or customize as needed. 

---

📦 Requirements
- Python (via FreeCAD or Fusion 360 environment)
- FreeCAD 0.20+ for FreeCAD scripts
-  Fusion 360 (latest) for add-ins
-  Basic understanding of Python and CAD modeling

#FreeCAD #Fusion360 #CADAutomation #PythonScripts #EngineeringTools #BOM #ParametricDesign
