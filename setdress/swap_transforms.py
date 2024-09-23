import bpy
C = bpy.context

if len(C.selected_objects) == 2:
    
    map = []
    
    for ob in C.selected_objects:
        map.append({
            'location': ob.location.copy(),
            'rotation_euler': ob.rotation_euler.copy(),
            'scale': ob.scale.copy()
        })
    
    C.selected_objects[0].location = map[1]['location']
    C.selected_objects[0].rotation_euler = map[1]['rotation_euler']
    C.selected_objects[0].scale = map[1]['scale']
    C.selected_objects[1].location = map[0]['location']
    C.selected_objects[1].rotation_euler = map[0]['rotation_euler']
    C.selected_objects[1].scale = map[0]['scale']
