import bpy

for ob in [o for o in bpy.context.selected_objects if o.type == 'MESH']:
    ob.active_material_index = 0
    for i in range(len(ob.material_slots)):
        with bpy.context.temp_override(object=ob):
            bpy.ops.object.material_slot_remove()
