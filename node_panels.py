import bpy


class NODEEDITOR_PT_Node_Tools(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "BpyUtils"
    bl_label = "Tools"

    @classmethod
    def poll(self, context):
        return bpy.context.area.type == "NODE_EDITOR"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "use_nodes")
        layout.prop(context.object, "selected_render_layer")

        make_prop = layout.operator(
            "node.auto_aov", text="Make AOV", icon="NODE_COMPOSITING")
        make_prop.update_fileoutput = False
        make_prop.select_renderlayer = context.object.selected_render_layer

        update_prop = layout.operator(
            "node.auto_aov", text="Update AOV", icon="NODE_COMPOSITING")
        update_prop.update_fileoutput = True
        update_prop.select_renderlayer = False


def register():
    bpy.utils.register_class(NODEEDITOR_PT_Node_Tools)
    bpy.types.Object.selected_render_layer = bpy.props.BoolProperty(
        name="Selected RenderLayer",
        description="Use selected render layer",
        default=False
    )


def unregister():
    bpy.utils.unregister_class(NODEEDITOR_PT_Node_Tools)
    del bpy.types.Object.selected_render_layer


if __name__ == '__main__':
    register()
