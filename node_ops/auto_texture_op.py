import bpy
from pathlib import Path
from pprint import pprint


valid_types = [".png", ".jpg"]
valid_maps = [
    (["albedo", "basecolor", "color"], "sRGB"),
    (["metallic"], "Non-Color"),
    (["roughness"], "Non-Color"),
    (["normal"], "Non-Color"),
    (["height"], "Non-Color"),
    (["opacity", "alpha"], "Non-Color")
]

map_conns = {
    tuple(valid_maps[0][0]): ["Color", "Base Color"],
    tuple(valid_maps[1][0]): ["Color", "Metallic"],
    tuple(valid_maps[2][0]): ["Color", "Roughness"],
    tuple(valid_maps[5][0]): ["Color", "Alpha"],

    tuple(valid_maps[3][0]): ["Color", "Color"],
    tuple(valid_maps[4][0]): ["Color", "Height"],
}


class AUTO_TEXTURE_NODE_OP(bpy.types.Operator):
    bl_idname = "node.auto_texture"
    bl_label = "Auto texture node"
    bl_options = {"REGISTER", "UNDO"}   # "INTERNAL"

    filepath: bpy.props.StringProperty(
        name="Filepath",
        description="Texture filepath",
        subtype="DIR_PATH",
        default=""
    )

    @classmethod
    def poll(cls, context):
        if context.scene.render.engine != "CYCLES":
            return False

        active_object = context.active_object
        return active_object is not None and active_object.type == 'MESH'

    def execute(self, context):
        filepath = Path(self.filepath).resolve()
        if not self.filepath or not filepath.is_dir():
            return {"FINISHED"}

        valid_maps = self.get_valid_maps(filepath)

        # Setup Material
        mats = bpy.data.materials
        self.material = mats.new(name=valid_maps.pop("Name", "Mat"))
        self.material.use_nodes = True
        self.nodes = self.material.node_tree.nodes
        self.links = self.material.node_tree.links

        material_output = self.nodes.get("Material Output")
        bsdf = self.nodes.get("Principled BSDF")

        # Setup Image Textures
        height_exist = ("Height" in valid_maps.keys())
        for map, map_info in sorted(valid_maps.items()):

            texture = self.create_texture(map, map_info[0], map_info[1])
            self.create_connections(bsdf, map, texture, height_exist)

        self.assign_material(context)

        return {"FINISHED"}

    def assign_material(self, context):
        active_object = context.active_object
        mat_slots = active_object.material_slots
        if mat_slots:
            try:
                idx = next(n for n, x in enumerate(mat_slots)
                           if not x.material)
                active_object.data.materials[idx] = self.material
            except StopIteration:
                active_object.data.materials.append(self.material)
        else:
            active_object.data.materials.append(self.material)

    def get_valid_maps(self, filepath):
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        valid_maps_dict = {"Name": filepath.stem}
        for i in filepath.iterdir():
            # file-check
            if not i.suffix.lower() in valid_types:
                continue

            # map-check
            if self.is_valid_map(i):
                valids = next([map, val_maps[1]]
                              for val_maps in valid_maps for map in val_maps[0] if map in i.stem.lower())
                valid_maps_dict[valids[0].title()] = [i, valids[1]]

        return valid_maps_dict

    def create_connections(self, shader, map, texture, height_exist):
        map = map.lower()
        outgoing, incoming = map_conns[next(
            x for x in map_conns.keys() if map in x)]

        if map == "height":
            bump = self.nodes.new("ShaderNodeBump")
            self.links.new(bump.inputs[incoming], texture.outputs[outgoing])
            texture = bump
            incoming = outgoing = "Normal"

        if map == "normal":
            normal = self.nodes.new("ShaderNodeNormalMap")
            self.links.new(normal.inputs[incoming], texture.outputs[outgoing])
            texture = normal

            if height_exist:
                shader = next(x for x in self.nodes.keys() if "Bump" in x)
                shader = self.nodes.get(shader)

            incoming = outgoing = "Normal"

        self.links.new(shader.inputs[incoming], texture.outputs[outgoing])

    def create_texture(self, map_type, map_path, colorspace):
        texture = self.nodes.new("ShaderNodeTexImage")
        texture.name = map_path.stem
        texture.image = bpy.data.images.load(str(map_path))
        texture.image.colorspace_settings.name = colorspace

        return texture

    @staticmethod
    def is_valid_map(infile):
        for i in valid_maps:
            for map in i[0]:
                if map in infile.stem.lower():
                    return True
        return False


def register():
    bpy.utils.register_class(AUTO_TEXTURE_NODE_OP)


def unregister():
    bpy.utils.unregister_class(AUTO_TEXTURE_NODE_OP)


if __name__ == '__main__':
    register()
