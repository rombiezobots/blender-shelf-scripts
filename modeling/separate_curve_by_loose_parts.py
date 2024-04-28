import bpy

selected_curves = [
    ob.data for ob in bpy.data.objects if ob.type == 'CURVE' and not (ob.data.library or ob.data.override_library)
]

for curve in selected_curves:
    for spline in curve.splines:
        # deselect all
        for spline in curve.splines:
            if spline.type == 'BEZIER':
                for p in spline.bezier_points:
                    p.select_control_point = False
            else:
                for p in spline.points:
                    p.select = False

        # select only this spline's points
        if spline.type == 'BEZIER':
            for p in spline.bezier_points:
                p.select_control_point = True
        else:
            for p in spline.points:
                p.select = True

        # separate
        bpy.ops.curve.separate()
