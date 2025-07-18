import adsk.core, adsk.fusion, traceback, math

def run(_context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent

        # Inputs
        num_teeth = 20
        module = 2.0              # mm
        pressure_angle_deg = 20  # degrees
        gear_thickness = 5.0     # mm
        bore_dia = 5.0           # mm
        backlash = 0.05          # mm

        pressure_angle_rad = math.radians(pressure_angle_deg)

        pitch_dia = num_teeth * module
        pitch_radius = pitch_dia / 2
        base_radius = pitch_radius * math.cos(pressure_angle_rad)
        addendum = module
        dedendum = 1.25 * module
        outer_radius = pitch_radius + addendum
        root_radius = pitch_radius - dedendum

        # Create Sketch
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        sketch.name = 'Involute Gear Sketch'

        center = adsk.core.Point3D.create(0, 0, 0)

        def involute_point(r_base, t):
            x = r_base * (math.cos(t) + t * math.sin(t))
            y = r_base * (math.sin(t) - t * math.cos(t))
            return adsk.core.Point3D.create(x, y, 0)

        involute_curve_pts = adsk.core.ObjectCollection.create()
        mirrored_curve_pts = adsk.core.ObjectCollection.create()
        max_angle = math.sqrt((outer_radius**2 / base_radius**2) - 1)
        num_points = 15

        for i in range(num_points + 1):
            t = i * max_angle / num_points
            pt = involute_point(base_radius, t)
            involute_curve_pts.add(pt)
        
            mirrored_curve_pts.add(adsk.core.Point3D.create(-pt.x, pt.y, 0))

        lines = sketch.sketchCurves.sketchLines
        spline = sketch.sketchCurves.sketchFittedSplines.add(involute_curve_pts)
        mirrored_spline = sketch.sketchCurves.sketchFittedSplines.add(mirrored_curve_pts)

        pt1 = involute_curve_pts.item(0)
        pt2 = mirrored_curve_pts.item(0)
        pt3 = involute_curve_pts.item(involute_curve_pts.count - 1)
        pt4 = mirrored_curve_pts.item(mirrored_curve_pts.count - 1)

        lines.addByTwoPoints(pt1, pt2)
        lines.addByTwoPoints(pt3, pt4)

       
        gear_profile = None
        for prof in sketch.profiles:
            if prof.profileLoops.count == 1:
                gear_profile = prof
                break

        if not gear_profile:
            ui.messageBox('⚠️ Could not find tooth profile.')
            return

        # Extrude
        extrudes = rootComp.features.extrudeFeatures
        tooth_input = extrudes.createInput(gear_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        tooth_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(gear_thickness))
        tooth_body = extrudes.add(tooth_input)

        tooth_collection = adsk.core.ObjectCollection.create()
        tooth_collection.add(tooth_body)

        z_axis = rootComp.zConstructionAxis
        circular_patterns = rootComp.features.circularPatternFeatures
        pattern_input = circular_patterns.createInput(tooth_collection, z_axis)
        pattern_input.quantity = adsk.core.ValueInput.createByReal(num_teeth)
        pattern_input.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        pattern_input.isSymmetric = False
        circular_patterns.add(pattern_input)

        bore_sketch = sketches.add(xyPlane)
        bore_sketch.name = "Bore"
        bore_sketch.sketchCurves.sketchCircles.addByCenterRadius(center, bore_dia / 2)

        bore_profile = bore_sketch.profiles.item(0)
        cut_input = extrudes.createInput(bore_profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        cut_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(gear_thickness + 0.1))
        extrudes.add(cut_input)

        ui.messageBox("Involute gear created successfully!")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
