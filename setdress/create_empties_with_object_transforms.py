import bpy

for ob in bpy.context.selected_objects:

    empty = bpy.data.objects.new(name=ob.name, object_data=None)

    empty.location = ob.location
    empty.rotation_euler = ob.rotation_euler
    empty.scale = ob.scale

    bpy.context.scene.collection.objects.link(empty)