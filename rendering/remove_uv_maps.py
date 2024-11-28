import bpy

C = bpy.context

if len(C.selected_objects) > 0:
    objects = [ob for ob in C.selected_objects if ob.type == 'MESH' and not (ob.library or ob.override_library)]
else:
    objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not (ob.library or ob.override_library)]

for ob in objects:
    for layer in ob.data.uv_layers:
        ob.data.uv_layers.remove(layer)