import bpy

bpy.ops.file.make_paths_absolute()

# Only images for now.
images = [img for img in bpy.data.images if not img.library and not img.override_library]
print(f'Checking {len(images)} images.')

roots = {
    '/projects/library/': [
        '/f/library/',
        '/l/',
        '/studio/library/',
        'F:/library/',
        'L:/',
    ],
    '/projects/local/': [
        '/w/projects/',
        'F:/',
        'F:/projects/',
        'W:/',
    ],
}
other_changes = {
    'char': ['character'],
    'elt': ['decoration', 'element'],
    'prop': ['animprop'],
    'seq': ['sequence'],
}

for img in images:
    print('----')
    print(f'Filepath is {img.filepath}')
    new_path = img.filepath

    for right, wrong in roots.items():
        for bad in wrong:
            if new_path.startswith(bad):
                new_path = new_path.replace(bad, right)
                break

    for right, wrong in other_changes.items():
        for bad in wrong:
            new_path = new_path.replace(bad, right)

    if new_path != img.filepath:
        print(f'Correcting to {new_path}')
        img.filepath = new_path

    print('----')
