import bpy
from mathutils import Vector
from math import sqrt, ceil


def half_dimensions(ob):
    bbox_ws = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
    xmax = bbox_ws[4][0]
    xmin = bbox_ws[0][0]
    ymax = bbox_ws[3][1]
    ymin = bbox_ws[0][1]
    return ((xmax - xmin) / 2, (ymax - ymin) / 2)


C = bpy.context

row_length = ceil(sqrt(len(C.selected_objects)))

ob_last = C.object
x_original = C.object.location[0]

for index, ob in enumerate([ob for ob in C.selected_objects if not ob == C.object]):

    half_width, half_depth = half_dimensions(ob)
    half_width_last, half_depth_last = half_dimensions(ob_last)

    ob.location = ob_last.location

    if (index + 1) % row_length == 0:
        ob.location[0] = x_original
        ob.location[1] += 1.5 * (half_depth_last + half_depth)
    else:
        ob.location[0] += 1.5 * (half_width_last + half_width)

    ob_last = ob
