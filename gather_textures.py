from pathlib import Path
import bpy
import re
import shutil

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
        'disp16',
        'displacement',
        'dsp',
        'dsp16',
    ],
    'NOR': [
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
        'opa',
        'overlay',
    ],
    'MTL': [
        'metallic',
        'metalness',
        'mtl',
    ],
}

dir_blend = bpy.path.abspath(path='//')
dir_textures = Path(dir_blend).parents[0] / 'textures'
dir_textures.mkdir(exist_ok=True)
print('===================================')
print(f'Source file is in {dir_blend}')
print(f'Textures go to {dir_textures}')

imgs_not_in_lib = [
    img for img in bpy.data.images if img.filepath != '' and not img.filepath.startswith('/projects/library/')
]

# =====================================================================================================================
# functions
# =====================================================================================================================


def list_to_string_camel_cased(segments: list):
    return ''.join(seg.capitalize() for seg in segments if seg.isalnum())


def keyword_and_acronym(file_name: str):
    '''Find the acronym first, then use it to slice off and glue together the keyword.'''
    segments = re.split('([^a-zA-Z0-9])', file_name)

    acronym = next(  # immediately assign the first match, we don't need a list
        (
            acronym_good
            for acronym_good, words_known in map.items()
            if any(seg.casefold() == word.casefold() for word in words_known for seg in segments)
        ),
        None,
    )

    acronym_index = next((i for i in reversed(range(len(segments))) if segments[i].lower() in map[acronym]), None)
    keyword_segments = segments[:acronym_index]
    keyword = list_to_string_camel_cased(keyword_segments)

    # print('Segments:', segments)
    # print('Acronym:', acronym)
    # print('Acronym index:', acronym_index)
    # print('Keyword segments:', keyword_segments)

    return keyword, acronym


# =====================================================================================================================
# script
# =====================================================================================================================


for img in imgs_not_in_lib:
    print('---------')
    print('Old file:', Path(img.filepath).stem)

    # --------
    # copy all images to a textures folder in this local version directory
    # --------

    try:
        # TODO: expand for udim images.
        filepath = shutil.copy(src=img.filepath, dst=dir_textures)
        img.filepath = bpy.path.abspath(path=str(filepath))
    except shutil.SameFileError:
        pass

    # --------
    # standardize file naming
    # --------

    filename_current = Path(img.filepath).stem

    keyword, acronym = keyword_and_acronym(file_name=filename_current)
    ext = Path(img.filepath).suffix

    # udim = next((seg for seg in segments if re.match(r'\d{4}', seg)), '1001')

    filepath_new = Path(dir_textures) / f'{keyword}_{acronym}{ext}'
    print('New file:', filepath_new)
    if not filepath_new.is_file():
        Path(img.filepath).rename(filepath_new)
