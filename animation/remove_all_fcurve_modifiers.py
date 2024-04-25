import bpy

for fcurve in bpy.context.object.animation_data.action.fcurves:
    for mod in fcurve.modifiers:
        fcurve.modifiers.remove(mod)
