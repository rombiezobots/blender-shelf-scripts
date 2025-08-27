import bpy

for ob in bpy.context.selected_objects:
    material_name = next(slot.material.name for slot in ob.material_slots)
    keyword = material_name.split('.')[0]
    ob.name = f'{keyword}.GEO.001'