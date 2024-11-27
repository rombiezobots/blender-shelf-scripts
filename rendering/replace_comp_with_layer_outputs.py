import bpy
from pathlib import Path

C = bpy.context
D = bpy.data

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
    outputs_available = [o.name for o in node_layer.outputs if o.enabled]
    for output_name in outputs_available:
        node_output.file_slots.new(output_name)
        C.scene.node_tree.links.new(node_output.inputs[output_name], node_layer.outputs[output_name])
        if 'Crypto' in output_name:
            node_output.format.color_depth = '32'
