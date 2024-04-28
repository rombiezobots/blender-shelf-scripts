import bpy

context = bpy.context
if len(context.selected_objects) > 0:
    objects = [ob for ob in context.selected_objects if ob.type == 'EMPTY' and not (ob.library or ob.override_library)]
else:
    objects = [ob for ob in bpy.data.objects if ob.type == 'EMPTY' and not (ob.library or ob.override_library)]
for ob in objects:
    ob.empty_display_size = 0
