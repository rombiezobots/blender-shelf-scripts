import bpy

for mat in bpy.data.materials:
    mat.displacement_method = 'DISPLACEMENT'