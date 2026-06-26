# Set all low-poly collections to Viewport Only
# Set all high-poly collections to Render Only

import bpy

for collection in bpy.data.collections:
    if 'lowpoly' in collection.name.lower():
        collection.hide_viewport = False
        collection.hide_render = True
    if 'highpoly' in collection.name.lower():
        collection.hide_viewport = True
        collection.hide_render = False
