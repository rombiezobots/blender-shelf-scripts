import bpy
import math

if len(bpy.context.selected_objects) > 0:
    objects = [ob for ob in bpy.context.selected_objects if not (ob.library or ob.override_library)]
else:
    objects = [ob for ob in bpy.data.objects if not (ob.library or ob.override_library)]
for ob in objects:
    for i in range(3):  # XYZ
        orig = ob.rotation_euler[i]
        ob.rotation_euler[i] = math.radians(90) * round(orig / math.radians(90))
