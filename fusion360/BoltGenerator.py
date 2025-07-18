"""This file acts as the main module for this script."""
import adsk.core, adsk.fusion, adsk.cam, traceback
import math

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        # ===== Prompt User for Inputs =====
        inputDlg = ui.inputBox(
            'Enter values separated by commas:\nBolt Diameter (mm), Bolt Length (mm), Head Width (AF mm), Head Height (mm)',
            'Bolt Generator Input',
            '10, 50, 17, 8'
        )

        values = [float(val.strip()) for val in inputDlg[0].split(',')]
        bolt_diameter, bolt_length, head_width, head_height = values

        # ===== Create New Component =====
        rootComp = design.rootComponent
        allOccs = rootComp.occurrences
        newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
        newComp = newOcc.component
        newComp.name = 'Parametric Bolt'

        # ===== Create Sketch =====
        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        center = adsk.core.Point3D.create(0, 0, 0)

        # ---- Draw Hex Head ----
        num_sides = 6
        radius = head_width / 2
        angle_step = 2 * math.pi / num_sides
        points = []

        for i in range(num_sides):
            angle = i * angle_step
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append(adsk.core.Point3D.create(x, y, 0))

        lines = sketch.sketchCurves.sketchLines
        for i in range(num_sides):
            pt1 = points[i]
            pt2 = points[(i + 1) % num_sides]
            lines.addByTwoPoints(pt1, pt2)

        # ---- Draw Shaft Circle ----
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(center, bolt_diameter / 2)

        # ===== Extrude Features =====
        profs = sketch.profiles
        hex_profile = None
        shaft_profile = None

        largest_area = 0
        smallest_area = float('inf')
        for prof in profs:
            area = prof.areaProperties().area
            if area > largest_area:
                largest_area = area
                hex_profile = prof
            if area < smallest_area:
                smallest_area = area
                shaft_profile = prof

        extrudes = newComp.features.extrudeFeatures

        # Shaft extrusion
        shaft_input = extrudes.createInput(shaft_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        shaft_distance = adsk.core.ValueInput.createByReal(bolt_length)
        shaft_input.setDistanceExtent(False, shaft_distance)
        shaft = extrudes.add(shaft_input)
        shaft.bodies.item(0).name = "Bolt Shaft"

        # Head extrusion
        head_input = extrudes.createInput(hex_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        head_distance = adsk.core.ValueInput.createByReal(head_height)
        head_input.setDistanceExtent(False, head_distance)
        head = extrudes.add(head_input)
        head.bodies.item(0).name = "Bolt Head"

        ui.messageBox('✅ Bolt created with your custom parameters!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
