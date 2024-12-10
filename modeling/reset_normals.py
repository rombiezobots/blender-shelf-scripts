import bpy

C = bpy.context
if len(C.selected_objects) > 0:
    objects = [ob for ob in C.selected_objects if ob.type == 'MESH' and not (ob.library or ob.override_library)]
else:
    objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not (ob.library or ob.override_library)]

for ob in objects:
    for edge in ob.data.edges:
        edge.use_edge_sharp = False
    C.view_layer.objects.active = ob
    bpy.ops.mesh.customdata_custom_splitnormals_clear()
