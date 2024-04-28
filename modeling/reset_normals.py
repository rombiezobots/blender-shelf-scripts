import bpy

context = bpy.context
mesh_objects = [
    ob for ob in context.selected_objects if ob.type == 'MESH' and not (ob.data.library or ob.data.override_library)
]
if len(mesh_objects) == 0:
    raise RuntimeError('This tool only works with a selection of mesh objects.')

for ob in mesh_objects:
    for edge in ob.data.edges:
        edge.use_edge_sharp = False
    ob.data.use_auto_smooth = False
    bpy.context.view_layer.objects.active = ob
    bpy.ops.mesh.customdata_custom_splitnormals_clear()
