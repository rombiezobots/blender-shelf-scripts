import bpy

context = bpy.context

if len(context.selected_objects) > 0:
    objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not (ob.library or ob.override_library)]
else:
    objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not (ob.library or ob.override_library)]

for ob in objects:
    subdiv_mods = [m for m in ob.modifiers if m.type == 'SUBSURF']
    for mod in subdiv_mods:
        mod.show_in_editmode = False
