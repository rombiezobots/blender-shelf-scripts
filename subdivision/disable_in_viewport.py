import bpy

print('Disabling subdiv in viewport')

meshes = [o for o in bpy.data.objects if o.type == 'MESH']

for mesh in meshes:
    for mod in mesh.modifiers:
        if mod.type == 'SUBSURF':
            mod.show_in_editmode = False
            mod.show_viewport = False
            mod.boundary_smooth = 'PRESERVE_CORNERS'
