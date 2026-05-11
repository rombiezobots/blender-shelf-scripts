from pathlib import Path
import bpy
import re

print('=========================')
print('UPDATING FLAMENCO RENDERS')
print('=========================')

# Regular expression to match Flamenco's folder naming.
regex = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}')

# Make all paths absolute.
bpy.ops.file.make_paths_absolute()

images = [img for img in bpy.data.images if img.type in ['MULTILAYER', 'IMAGE']]
for img in images:

    print(f'Image {img.name}')

    # Skip Render Result and Viewer Node, as well as image datablocks with an empty filepath.
    if not img.filepath or img.filepath == '' or img.is_missing:
        continue

    # Get the latest date_time formatted folder in the image's grandparent folder.
    parent_dir = Path(img.filepath).parents[1]
    contents = sorted(parent_dir.iterdir(), reverse=True)
    latest_path = next((dir for dir in contents if dir.is_dir() and regex.match(dir.stem)), None)
    if not latest_path:
        continue

    # If the current image is not in the latest Flamenco folder, update the filepath.
    name_current_folder = Path(img.filepath).parent.stem
    name_latest_folder = latest_path.stem
    if name_current_folder != name_latest_folder:
        print('Updating', img.name, 'from', name_current_folder, 'to', name_latest_folder)
        filename = Path(img.filepath).name
        img.filepath = str(latest_path / filename)
