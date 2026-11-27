import bpy

for ob in bpy.context.selected_objects:
    if hasattr(ob, 'animation_data'):
        ob.animation_data.action = None