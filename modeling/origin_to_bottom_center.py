import bpy
from mathutils import Matrix, Vector

# Moves the origin of each selected mesh or curve object to the bottom center of its bounding box, measured in the
# object's own space, so the result is the same as if the object's rotation and scale were applied after setting the
# origin. The geometry stays where it is in the world.

context = bpy.context
objects = [
    ob
    for ob in context.selected_objects
    if ob.type in ['MESH', 'CURVE'] and not (ob.data.library or ob.data.override_library)
]
if len(objects) == 0:
    raise RuntimeError('This tool only works with a selection of mesh or curve objects.')

# Objects can share their data, which may only be moved once. Every object using it, selected or not, then gets the
# same correction, so none of them visibly moves.
data_objects = {}
for ob in objects:
    data_objects.setdefault(ob.data, ob)

for data, ob in data_objects.items():
    # The bounding box is in the object's local space: take the center of its width and depth, and its lowest point.
    corners = [Vector(corner) for corner in ob.bound_box]
    offset = Vector(
        (
            (min(c.x for c in corners) + max(c.x for c in corners)) / 2,
            (min(c.y for c in corners) + max(c.y for c in corners)) / 2,
            min(c.z for c in corners),
        )
    )
    if offset.length == 0:
        continue

    # Move the geometry so that point becomes the origin, then move the objects (and the parent inverse of their
    # children) the other way, so nothing changes in world space.
    data.transform(Matrix.Translation(-offset))
    data.update_tag()
    for user in [o for o in bpy.data.objects if o.data == data]:
        user.matrix_basis = user.matrix_basis @ Matrix.Translation(offset)
        for child in user.children:
            child.matrix_parent_inverse = Matrix.Translation(-offset) @ child.matrix_parent_inverse
