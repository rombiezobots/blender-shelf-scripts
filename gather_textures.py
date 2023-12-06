import bpy
import shutil
from pathlib import Path
import re

# =====================================================================================================================
# variables
# =====================================================================================================================

map = {
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
        'displacement',
        'dsp',
    ],
    'NOR': [
        'nor',
        'normal',
        'normals',
        'nrm',
    ],
    'MTL': [
        'metallic',
        'mtl',
    ],
    'SPR': [
        'rough',
        'roughness',
        'spr',
    ],
}

dir_blend = bpy.path.abspath(path='//')
dir_textures = Path(dir_blend) / 'textures'
dir_textures.mkdir(exist_ok=True)
print(f'Source file is in {dir_blend}')
print(f'Textures go to {dir_textures}')

imgs_not_in_lib = [
    img for img in bpy.data.images if img.filepath != '' and not img.filepath.startswith('/projects/library/')
]

# =====================================================================================================================
# functions
# =====================================================================================================================


def camel_case(input: str):
    return


def keyword_and_acronym(segments: list):
    '''Return the first standardized acronym that matches a known arbitrary denominator in the file name'''
    # TODO: expand function to treat everything before the acronym (whatever was used) as the keyword.
    return next(
        (acro for acro, words in map.items() if any(searched == word for word in words for searched in segments)),
        'NONE',
    )


# =====================================================================================================================
# script
# =====================================================================================================================


for img in imgs_not_in_lib:
    print('----------------')
    print('Old file: ', Path(img.filepath).stem)

    # copy all images to a textures folder in this local version directory
    # TODO: expand for udim images.
    try:
        filepath = shutil.copy(src=img.filepath, dst=dir_textures)
        img.filepath = bpy.path.abspath(path=str(filepath))
    except shutil.SameFileError:
        pass

    # standardize file naming
    segments = Path(img.filepath).stem.split('.')[0].split('_')
    keyword = segments[0]
    acronym = keyword_and_acronym(segments=segments)
    udim = next((seg for seg in segments if re.match(r'\d{4}', seg)), '1001')
    new_file_name = f'{keyword}_{acronym}.{udim}'
    print('New file: ', new_file_name)
