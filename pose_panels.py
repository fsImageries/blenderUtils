import bpy


class VIEW3D_PT_Pose_Tools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BpyUtils"
    bl_label = "Tools"

    @classmethod
    def poll(self, context):
        return (bpy.context.area.type == "VIEW_3D" and context.active_object.mode == "POSE")

    def draw(self, context):
        layout = self.layout
        ob = context.object

        snap_prop = layout.operator(
            "pose.pose_snap", text="Bone Snap", icon="BONE_DATA")
        snap_prop.pose_snap_translation = ob.pose_snap_translation
        snap_prop.pose_snap_rotation = ob.pose_snap_rotation
        snap_prop.pose_snap_scale = ob.pose_snap_scale

        layout.prop(ob, "pose_snap_translation")
        layout.prop(ob, "pose_snap_rotation")
        layout.prop(ob, "pose_snap_scale")


def register():
    bpy.utils.register_class(VIEW3D_PT_Pose_Tools)

    bpy.types.Object.pose_snap_translation = bpy.props.BoolProperty(
        name="Translation",
        description="Set translation snap",
        default=True
    )
    bpy.types.Object.pose_snap_rotation = bpy.props.BoolProperty(
        name="Rotation",
        description="Set rotation snap",
        default=True
    )
    bpy.types.Object.pose_snap_scale = bpy.props.BoolProperty(
        name="Scale",
        description="Set scale snap",
        default=True
    )


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_Pose_Tools)

    del bpy.types.Object.pose_snap_translation
    del bpy.types.Object.pose_snap_rotation
    del bpy.types.Object.pose_snap_scale


if __name__ == '__main__':
    register()
