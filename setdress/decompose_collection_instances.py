"""
Turn a collection-instance object into a real collection, in place.

Given an Empty (or any object) with instance_type == 'COLLECTION', this
builds a new Collection that mirrors the instanced collection exactly:
copies of its objects and of its child collections, transformed as the
instance placed them. Only that one level of instancing is undone: any
collection-instance objects inside the collection are copied as
collection instances, so the result looks the same as before.

Run as a script, it decomposes every selected collection instance.

Usage:
    import bpy
    from decompose_collection_instances import instance_to_collection, instances_to_collections

    instance_to_collection(bpy.context.active_object)
    instances_to_collections(bpy.context.selected_objects)
"""

import bpy
from mathutils import Matrix


def _copy_object(obj, world_matrix, link_data=True):
    """Duplicate a single object and place it at an explicit world
    matrix, unparented (parenting among duplicates is restored later
    where applicable)."""
    obj_copy = obj.copy()
    if not link_data and obj.data is not None:
        obj_copy.data = obj.data.copy()
    obj_copy.parent = None
    obj_copy.matrix_parent_inverse = Matrix.Identity(4)
    obj_copy.matrix_world = world_matrix
    return obj_copy


def _realize_collection(src_col, matrix, name, obj_map, link_data=True, _depth=0, _max_depth=64):
    """
    Build a new collection mirroring src_col's contents (objects + child
    collections), with `matrix` already including any instance_offset
    correction needed to place src_col's local space in world space.
    Collection-instance objects are copied as they are, not realized.
    """
    if _depth > _max_depth:
        raise RecursionError(
            f"Collection nesting exceeds {_max_depth} levels (possible cycle involving '{src_col.name}')"
        )

    new_col = bpy.data.collections.new(name)
    level_map = {}  # old -> new, objects created at *this* level only

    for obj in src_col.objects:
        world = matrix @ obj.matrix_world
        obj_copy = _copy_object(obj, world, link_data=link_data)
        new_col.objects.link(obj_copy)
        level_map[obj] = obj_copy
        obj_map[obj] = obj_copy

    # Re-parent duplicates to each other where both ends were duplicated
    # at this level, preserving the world matrices already set.
    for obj, obj_copy in level_map.items():
        if obj.parent in level_map:
            new_parent = level_map[obj.parent]
            world = obj_copy.matrix_world.copy()
            obj_copy.parent = new_parent
            obj_copy.matrix_parent_inverse = new_parent.matrix_world.inverted()
            obj_copy.matrix_world = world

    # Child collections nested in the outliner.
    for child_col in src_col.children:
        nested_col = _realize_collection(
            child_col,
            matrix,
            child_col.name,
            obj_map,
            link_data=link_data,
            _depth=_depth + 1,
            _max_depth=_max_depth,
        )
        new_col.children.link(nested_col)

    return new_col


def _remap_references(obj_map):
    """Best-effort: repoint modifiers/constraints at duplicated objects
    instead of the originals, whenever both ends were duplicated."""
    for obj_copy in obj_map.values():
        for mod in obj_copy.modifiers:
            for attr in ("object", "target", "mask_object", "mirror_object"):
                target = getattr(mod, attr, None)
                if target in obj_map:
                    setattr(mod, attr, obj_map[target])
        for con in obj_copy.constraints:
            target = getattr(con, "target", None)
            if target in obj_map:
                con.target = obj_map[target]


def instance_to_collection(inst_obj, new_name=None, link_data=True, remap_references=True, remove_original=True):
    """
    Replace a collection-instance object, in place, with a new collection
    mirroring the collection it instanced. Collection instances inside it
    stay collection instances.

    Args:
        inst_obj: the collection-instance object to realize.
        new_name: name for the resulting top-level collection
                  (defaults to the instanced collection's name).
        link_data: if True, duplicates share object-data blocks
                   (like Alt+D). If False, each duplicate gets its own
                   independent data-block (like Shift+D).
        remap_references: if True, best-effort repoint modifiers'/
                   constraints' object references at duplicates when
                   both ends were duplicated together.
        remove_original: if True, delete the original instance-empty
                   after building its replacement.

    Returns:
        The newly created top-level bpy.types.Collection.
    """
    if inst_obj.instance_type != 'COLLECTION' or inst_obj.instance_collection is None:
        raise ValueError(f"'{inst_obj.name}' is not a collection-instance object")

    bpy.context.view_layer.update()  # ensure matrix_world values are current

    src_col = inst_obj.instance_collection
    matrix = inst_obj.matrix_world @ Matrix.Translation(-src_col.instance_offset)
    name = new_name or src_col.name

    obj_map = {}
    new_col = _realize_collection(src_col, matrix, name, obj_map, link_data=link_data)

    if remap_references:
        _remap_references(obj_map)

    # Link the new collection wherever the instance object used to live.
    parents = list(inst_obj.users_collection)
    for parent in parents:
        parent.children.link(new_col)

    if remove_original:
        for parent in parents:
            parent.objects.unlink(inst_obj)
        bpy.data.objects.remove(inst_obj, do_unlink=True)

    return new_col


def instances_to_collections(objects, **kwargs):
    """Run instance_to_collection on every collection-instance object in
    `objects`, skipping the rest. Returns the new collections."""
    instances = [obj for obj in objects if obj.instance_type == 'COLLECTION' and obj.instance_collection is not None]
    return [instance_to_collection(obj, **kwargs) for obj in instances]


if __name__ == "__main__":
    if not instances_to_collections(bpy.context.selected_objects):
        raise RuntimeError("No collection instances selected")
