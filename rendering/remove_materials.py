import bpy

C = bpy.context

mesh_objects = [
    ob
    for ob in C.selected_objects
    if ob.type in ['MESH', 'CURVE'] and not (ob.data.library or ob.data.override_library)
]

for ob in mesh_objects:
    ob.data.materials.clear()
