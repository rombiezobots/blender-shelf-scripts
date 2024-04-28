import bpy

context = bpy.context
if len(context.selected_objects) > 0:
    objects = [ob for ob in context.selected_objects if not (ob.library or ob.override_library)]
else:
    objects = [ob for ob in bpy.data.objects if not (ob.library or ob.override_library)]
for ob in objects:
    collections = [coll for coll in bpy.data.collections if ob.name in coll.objects]
    for coll in collections:
        coll.instance_offset = ob.location
