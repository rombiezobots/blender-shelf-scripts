import bpy

context = bpy.context

if len(context.selected_objects) > 0:
    objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not (ob.library or ob.override_library)]
else:
    objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not (ob.library or ob.override_library)]

old = context.scene.tool_settings.use_transform_data_origin
context.scene.tool_settings.use_transform_data_origin = True

for ob in objects:
    context.view_layer.active_object = ob
    bpy.ops.transform.transform(mode='ALIGN')

context.scene.tool_settings.use_transform_data_origin = old
