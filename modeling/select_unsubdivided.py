import bpy

context = bpy.context
objects = [
    ob for ob in context.scene.objects if ob.type == 'MESH' and not (ob.data.library or ob.data.override_library)
]

bpy.ops.object.select_all(action='DESELECT')

for ob in objects:
    has_enabled_subsurf_modifiers = False
    for mod in ob.modifiers:
        if mod.type == 'SUBSURF':
            has_enabled_subsurf_modifiers = mod.show_render and (
                mod.render_levels > 0 or ob.cycles.use_adaptive_subdivision
            )
            break
    if ob.name in context.view_layer.objects:
        ob.select_set(not has_enabled_subsurf_modifiers)
