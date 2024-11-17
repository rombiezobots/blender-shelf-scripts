import bpy


def sort_collection(collection):
    '''Recursive function that unlinks and relinks every sub
    collection, then proceeds to repeat itself on that collection.'''

    if not collection.children:
        return

    children = sorted(
        [c for c in collection.children if not c.library and not c.override_library], key=lambda c: c.name
    )
    for child in children:
        collection.children.unlink(child)
        collection.children.link(child)
        sort_collection(child)


sort_collection(bpy.context.scene.collection)
