import bpy
from pathlib import Path

C = bpy.context
D = bpy.data

x = 500
y = -350

# Enable compositing
C.scene.render.use_compositing = True

# Clear the whole compositing tree
C.scene.compositing_node_group.nodes.clear()

# Only do this for every layer that's enabled
layers = [l for l in C.scene.view_layers if l.use]
for i, layer in enumerate(layers):
    # Add a Render Layers node
    node_layer = C.scene.compositing_node_group.nodes.new('CompositorNodeRLayers')
    node_layer.name = f'layer_{layer.name}'
    node_layer.label = layer.name
    node_layer.layer = layer.name
    node_layer.location = (0, i * y)

    # Add a File Output node
    node_output = C.scene.compositing_node_group.nodes.new('CompositorNodeOutputFile')
    node_output.name = f'output_{layer.name}'
    node_output.label = layer.name
    node_output.format.file_format = 'OPEN_EXR_MULTILAYER'
    node_output.format.color_depth = '16'
    node_output.format.exr_codec = 'ZIP'
    node_output.directory = str(Path(C.scene.render.filepath).parent / layer.name)
    node_output.file_name = 'frame_'
    node_output.location = (x, i * y)

    # Include all passes enabled for this layer
    node_output.file_output_items.clear()

    for o in node_layer.outputs:
        if not o.enabled:
            continue
        node_output.file_output_items.new(socket_type=o.type if o.type != 'VALUE' else 'FLOAT', name=o.name)
        C.scene.compositing_node_group.links.new(node_output.inputs[o.name], node_layer.outputs[o.name])
        if 'Crypto' in o.name:
            node_output.format.color_depth = '32'
