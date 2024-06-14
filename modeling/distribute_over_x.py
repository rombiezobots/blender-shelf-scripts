import bpy
from mathutils import Vector

C = bpy.context


def bbox_width(ob):
    bbox_ws = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
    xmin = bbox_ws[0][0]
    xmax = bbox_ws[4][0]
    return xmax - xmin


# Get the widest width
widest_width = max([bbox_width(ob) for ob in C.selected_objects])

ob_last = C.object
for ob in [ob for ob in C.selected_objects if not ob == C.object]:
    ob.location = ob_last.location
    ob.location[0] += widest_width * 1.5
    ob_last = ob
