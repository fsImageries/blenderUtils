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

        box = layout.box()
        row = box.row()
        snap_prop = row.operator(
            "pose.pose_snap", text="Bone Snap", icon="BONE_DATA")
        snap_prop.pose_snap_translation = ob.pose_snap_translation
        snap_prop.pose_snap_rotation = ob.pose_snap_rotation
        snap_prop.pose_snap_scale = ob.pose_snap_scale

        row = box.row()
        row.prop(ob, "pose_snap_translation")
        row = box.row()
        row.prop(ob, "pose_snap_rotation")
        row = box.row()
        row.prop(ob, "pose_snap_scale")

        layout.separator()

        box = layout.box()
        row = box.row()
        pose_chain_prop = row.operator(
            "pose.bone_chain_constraint", text="Bone Chain Constraint", icon="BONE_DATA")
        pose_chain_prop.bone_chain_constraint__constraint_type = ob.bone_chain_constraint__constraint_type
        pose_chain_prop.bone_chain_constraint__target_suffix = ob.bone_chain_constraint__target_suffix
        pose_chain_prop.bone_chain_constraint__excludes = ob.bone_chain_constraint__excludes

        row = box.row()
        row.prop(ob, "bone_chain_constraint__constraint_type")
        row = box.row()
        row.prop(ob, "bone_chain_constraint__target_suffix")
        row = box.row()
        row.prop(ob, "bone_chain_constraint__excludes")


def register():
    bpy.utils.register_class(VIEW3D_PT_Pose_Tools)

    # Pose Snap Properties
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

    # Pose Chain Constraint Properties
    bpy.types.Object.bone_chain_constraint__constraint_type = bpy.props.StringProperty(
        name="Constraint Type",
        description="Define which constraint should be applied.",
        default="COPY_TRANSFORMS"
    )

    bpy.types.Object.bone_chain_constraint__target_suffix = bpy.props.StringProperty(
        name="Target Suffix",
        description="Define which suffix or prefix (doesn't matter) should be searched.",
        default="TGT"
    )

    bpy.types.Object.bone_chain_constraint__excludes = bpy.props.StringProperty(
        name="Exclude",
        description="Define, comma seperated, joints which can be skipped. Case-sensitive, not word-length sensitive.",
        default=""
    )


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_Pose_Tools)

    del bpy.types.Object.pose_snap_translation
    del bpy.types.Object.pose_snap_rotation
    del bpy.types.Object.pose_snap_scale

    del bpy.types.Object.bone_chain_constraint__constraint_type
    del bpy.types.Object.bone_chain_constraint__target_suffix
    del bpy.types.Object.bone_chain_constraint__excludes


if __name__ == '__main__':
    register()
