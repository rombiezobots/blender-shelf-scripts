from pathlib import Path
from pprint import pprint
import bpy
import re
import shutil

# =====================================================================================================================
# variables
# =====================================================================================================================

map_acronyms = {
    'COL': [
        'albedo',
        'basecol',
        'basecolor',
        'basecolour',
        'col',
        'color',
        'colour',
        'dif',
        'diff',
    ],
    'DSP': [
        'disp',
        'disp16',
        'displacement',
        'dsp',
        'dsp16',
    ],
    'NRM': [
        'nor',
        'normal',
        'normals',
        'nrm',
    ],
    'SPI': [
        'refl',
        'reflectivity',
        'spc',
        'spec',
        'specular',
        'spi',
    ],
    'SPG': [
        'gloss',
        'glossiness',
        'spg',
    ],
    'SPR': [
        'rough',
        'roughness',
        'spr',
    ],
    'OPA': [
        'alpha',
        'msk',
        'opa',
        'overlay',
    ],
    'MTL': [
        'metallic',
        'metalness',
        'mtl',
    ],
    'BUP': [
        'bump',
        'bup',
        'height',
        'hght',
    ],
    'ANI': [
        'ani',
        'anisotropy',
    ],
}

images_gathered = {}

dir_blend = bpy.path.abspath(path='//')
dir_textures = Path(dir_blend).parents[0] / 'textures'
dir_textures.mkdir(exist_ok=True)
print('===================================')
print(f'Source file is in {dir_blend}')
print(f'Textures go to {dir_textures}')

bpy.ops.file.make_paths_absolute()
imgs = [
    img
    for img in bpy.data.images
    if not img.filepath == ''
    and (
        not (img.filepath.startswith('/projects/library/') or img.filepath.startswith('/render/'))
        or (
            img.filepath.startswith(str(dir_textures))
            and re.match(r'[a-zA-Z0-9]+_[A-Z]{3}.[0-9]{4}', Path(img.filepath).stem)
        )
    )
]

# =====================================================================================================================
# functions
# =====================================================================================================================


def list_to_string_camel_cased(segments: list):
    return ''.join(seg.capitalize() for seg in segments if seg.isalnum())


def get_tokens_from_filepath(filepath: str):
    '''Find the acronym first, then use it to slice off and glue together the keyword.'''
    segments = re.split(r'[\._\-]', filepath)

    acronym = next(
        (
            acronym_good
            for acronym_good, words_known in map_acronyms.items()
            if any(seg.casefold() == word.casefold() for word in words_known for seg in segments)
        ),
        None,
    )

    if acronym:
        acronym_index = next(
            (i for i in reversed(range(len(segments))) if segments[i].lower() in map_acronyms[acronym]), None
        )
        keyword_segments = segments[:acronym_index]
        keyword = list_to_string_camel_cased(keyword_segments)
        return keyword, acronym

    raise ValueError(f'No acronym could be determined for {filepath}.')


# =====================================================================================================================
# script
# =====================================================================================================================


for img in imgs:
    files = []
    filepath_old = Path(img.filepath)
    filepath_new = None
    extension = filepath_old.suffix
    stem = Path(img.filepath).stem
    keyword, acronym = get_tokens_from_filepath(filepath=stem)

    # --------
    # Add all matching files for this image datablock to the dict.
    # UDIM tokens are switched to a glob pattern to collect all the files.
    # Also determine the new name.
    # --------

    if '<UDIM>' in stem:
        pattern = stem.replace('<UDIM>', '????')
        files += list(filepath_old.parents[0].glob(pattern))
        filepath_new = dir_textures / f'{keyword}_{acronym}.<UDIM>{extension}'
        img.source = 'TILED'
    else:
        files.append(filepath_old)
        filepath_new = dir_textures / f'{keyword}_{acronym}.1001{extension}'
        img.source = 'FILE'

    images_gathered[img.name] = {
        'filepath_new': filepath_new,
        'files': files,
        'datablock': img,
    }

pprint(images_gathered)

# --------
# Iterate over the dict and copy and rename all the files.
# --------

# for gathered in images_gathered.values():
#     for file in gathered['files']:
#         if not gathered['filepath_new'].is_file():
#             shutil.copyfile(src=file, dst=gathered['filepath_new'])  # TODO: EXPAND THE UDIM TOKEN! It's <UDIM> here.
#         gathered['datablock'].filepath = bpy.path.abspath(path=str(gathered['filepath_new']))  # Here that's fine.
