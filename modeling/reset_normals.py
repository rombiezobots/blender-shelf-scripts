import bpy

mesh_objects = [ob for ob in bpy.data.objects if ob.type == 'MESH']

for ob in mesh_objects:
    
    for edge in ob.data.edges:
        edge.use_edge_sharp = False
    
    ob.data.use_auto_smooth = False
    
    bpy.context.view_layer.objects.active = ob
    bpy.ops.mesh.customdata_custom_splitnormals_clear()