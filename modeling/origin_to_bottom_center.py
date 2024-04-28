import bpy
import copy
from mathutils import Vector

context = bpy.context
objects = [
    ob for ob in context.selected_objects if ob.type == 'MESH' and not (ob.data.library or ob.data.override_library)
]
if len(objects) == 0:
    raise RuntimeError('This tool only works with a selection of mesh objects.')

# Deselect all objects first, otherwise each of their origins will be
# overwritten by the current object in the loop. Also save a copy of the
# 3D Cursor's location.
for ob in objects:
    ob.select_set(False)
cursor_original = copy.copy(context.scene.cursor.location)

# Loop over each object.
for ob in objects:
    # Save a copy of the object's original location.
    object_original = copy.copy(ob.location)

    # Calculate the world space coordinates of its bounding box, take
    # half of its width and depth, and its lowest point.
    bbox_ws = [ob.matrix_world @ Vector(corner) for corner in ob.bound_box]
    xmax = bbox_ws[4][0]
    xmin = bbox_ws[0][0]
    ymax = bbox_ws[3][1]
    ymin = bbox_ws[0][1]
    zmin = bbox_ws[0][2]
    x = xmax - (xmax - xmin) / 2
    y = ymax - (ymax - ymin) / 2

    # Snap the 3D cursor to these coordinates, select the object, set its
    # origin, and deselect it again.
    context.scene.cursor.location = (x, y, zmin)
    ob.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    ob.select_set(False)

# Select the list of objects again, and restore the 3D Cursor.
for ob in objects:
    ob.select_set(True)
context.scene.cursor.location = cursor_original
