import bpy

bpy.ops.file.make_paths_absolute()
for lib in bpy.data.libraries:
    pt = common.pref(key=lib.flowdrops.path_template)
    tokens = files.token.extract(path=lib.filepath, pt=pt)
    if not tokens:
        common.log(f'Not a valid pipeline path: {lib.filepath}')
        continue
    # Replace the root, and look for the most recent version in the
    # resulting path. This version can be lower or higher than the
    # current local version.
