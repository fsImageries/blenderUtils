import bpy
from pathlib import Path


class AUTO_AOV_OP(bpy.types.Operator):
    bl_idname = "node.auto_aov"
    bl_label = "Auto aov setup"
    
    update_fileoutput: bpy.props.BoolProperty(
        name="Update",
        description="Update selected fileoutput",
        default=False
    )
    
    select_renderlayer: bpy.props.BoolProperty(
        name="RenderLayer",
        description="Use selected render layer",
        default=False
    )
    
    @classmethod
    def poll(cls, context):
        if not context.scene.use_nodes:
            return False
        try:
            next(x for x in context.scene.node_tree.nodes if "Render Layers" in x.name)
        except StopIteration:
            return False
        return True


    def execute(self, context):
        tree = context.scene.node_tree
        render_layer = next(x for x in tree.nodes if "Render Layers" in x.name)
        
        if self.select_renderlayer:
            if context.selected_nodes:
                render_layer = context.selected_nodes[0]  
        
        if self.update_fileoutput:
            fileoutput = context.selected_nodes[0]
            if fileoutput.type != "OUTPUT_FILE":
                try:
                    if not fileoutput.type == "R_LAYERS":
                        raise StopIteration
                    render_layer = fileoutput
                    fileoutput = next(i.to_node for i in tree.links if i.to_node.type == "OUTPUT_FILE" and i.from_node.name == render_layer.name)
                except StopIteration:
                    print("Please select a fileoutput node.")
                    return {"FINISHED"}
            elif fileoutput.type == "OUTPUT_FILE":
                try:
                    render_layer = next(i.from_node for i in tree.links if i.to_node.name == fileoutput.name and i.from_node.type == "R_LAYERS")
                except StopIteration:
                    print("Please select a fileoutput node.")
                    return {"FINISHED"}
        else:
            fileoutput = self.mk_fileout(tree)
        
        filepath = context.scene.render.filepath
        self.update_fileout(fileoutput, Path(filepath), tree, render_layer)
        
        return {"FINISHED"}
    
    @staticmethod
    def mk_fileout(tree):
        fileoutput = tree.nodes.new(type = "CompositorNodeOutputFile")
        fileoutput.format.file_format = "OPEN_EXR_MULTILAYER"
        
        return fileoutput
    
    @staticmethod
    def update_fileout(fileoutput, filepath, tree, render_layer):         
         fileoutput.base_path = str(filepath.parent / "aov")
         
         for out in render_layer.outputs:
            if not out.enabled: continue
            if fileoutput.inputs.get(out.name, None) is None:
                fileoutput.layer_slots.new(out.name)
                
            tree.links.new(render_layer.outputs[out.name], fileoutput.inputs[out.name])
        
         for ins in fileoutput.inputs.values():
             if not render_layer.outputs[ins.name].enabled:
                 fileoutput.layer_slots.remove(ins)
        
        
def register():
    bpy.utils.register_class(AUTO_AOV_OP)


def unregister():
    bpy.utils.unregister_class(AUTO_AOV_OP)


if __name__ == '__main__':
    register()
