import bpy
from pathlib import Path

C = bpy.context
D = bpy.data

map_settings_outputs = {
    # TODO: add AOVs, light groups
    'cycles.denoising_store_passes': ['Denoising Normal', 'Denoising Albedo', 'Denoising Depth'],
    'cycles.pass_debug_sample_count': ['Debug Sample Count'],
    'cycles.use_pass_shadow_catcher': ['Shadow Catcher', 'Noisy Shadow Catcher'],
    'cycles.use_pass_volume_direct': ['VolumeDir'],
    'cycles.use_pass_volume_indirect': ['VolumeInd'],
    'use_pass_ambient_occlusion': ['AO'],
    'use_pass_combined': ['Image'],
    'use_pass_diffuse_color': ['DiffCol'],
    'use_pass_diffuse_direct': ['DiffDir'],
    'use_pass_diffuse_indirect': ['DiffInd'],
    'use_pass_emit': ['Emit'],
    'use_pass_environment': ['Env'],
    'use_pass_glossy_color': ['GlossCol'],
    'use_pass_glossy_direct': ['GlossDir'],
    'use_pass_glossy_indirect': ['GlossInd'],
    'use_pass_material_index': ['IndexMA'],
    'use_pass_mist': ['Mist'],
    'use_pass_normal': ['Normal'],
    'use_pass_object_index': ['IndexOB'],
    'use_pass_position': ['Position'],
    'use_pass_transmission_color': ['TransCol'],
    'use_pass_transmission_direct': ['TransDir'],
    'use_pass_transmission_indirect': ['TransInd'],
    'use_pass_uv': ['UV'],
    'use_pass_vector': ['Vector'],
    'use_pass_z': ['Depth'],
    'use_pass_cryptomatte_material': [
        'CryptoMaterial00',
        'CryptoMaterial01',
        'CryptoMaterial02',
        'CryptoMaterial03',
        'CryptoMaterial04',
        'CryptoMaterial05',
        'CryptoMaterial06',
        'CryptoMaterial07',
    ],
    'use_pass_cryptomatte_object': [
        'CryptoObject00',
        'CryptoObject01',
        'CryptoObject02',
        'CryptoObject03',
        'CryptoObject04',
        'CryptoObject05',
        'CryptoObject06',
        'CryptoObject07',
    ],
    'use_pass_cryptomatte_asset': [
        'CryptoAsset00',
        'CryptoAsset01',
        'CryptoAsset02',
        'CryptoAsset03',
        'CryptoAsset04',
        'CryptoAsset05',
        'CryptoAsset06',
        'CryptoAsset07',
    ],
}


x = 500
y = -350

# Enable compositing
C.scene.render.use_compositing = True
C.scene.use_nodes = True

# Clear the whole compositing tree
C.scene.node_tree.nodes.clear()

# Only do this for every layer that's enabled
layers = [l for l in C.scene.view_layers if l.use]
for i, layer in enumerate(layers):

    # Add a Render Layers node
    node_layer = C.scene.node_tree.nodes.new('CompositorNodeRLayers')
    node_layer.name = f'layer_{layer.name}'
    node_layer.label = layer.name
    node_layer.layer = layer.name
    node_layer.location = (0, i * y)

    # Add a File Output node
    node_output = C.scene.node_tree.nodes.new('CompositorNodeOutputFile')
    node_output.name = f'output_{layer.name}'
    node_output.label = layer.name
    node_output.format.file_format = 'OPEN_EXR_MULTILAYER'
    node_output.format.color_depth = '16'
    node_output.format.exr_codec = 'ZIP'
    node_output.base_path = str(Path(C.scene.render.filepath).parent / layer.name / 'frame_')
    node_output.location = (x, i * y)

    # Include all passes enabled for this layer
    node_output.file_slots.clear()
    render_passes = [p for check, p in map_settings_outputs.items() if getattr(layer, check, False)]
    for pass_outputs in render_passes:
        for pass_output in pass_outputs:
            if node_layer.outputs.get(pass_output):
                node_output.file_slots.new(pass_output)
                C.scene.node_tree.links.new(node_output.inputs[pass_output], node_layer.outputs[pass_output])
