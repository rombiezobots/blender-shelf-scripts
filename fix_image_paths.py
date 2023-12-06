import bpy

bpy.ops.file.make_paths_absolute()

# Only images for now.
images = [img for img in bpy.data.images if not img.library and not img.override_library]
print(f'Checking {len(images)} images.')

root_fixing = {
    '/projects/library/': ['L:/', 'F:/library/', '/studio/library/', '/f/library/', '/l/'],
    '/projects/local/': ['W:/', 'F:/', '/w/projects/', 'F:/projects/'],
}
other_changes = {'prop': ['animprop'], 'elt': ['decoration', 'element']}

for img in images:
    print('----')
    print(f'Filepath is {img.filepath}')
    new_path = img.filepath

    for right, wrong in root_fixing.items():
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
