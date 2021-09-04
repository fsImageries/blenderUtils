import bpy


class Pose_Orient_Snap_OP(bpy.types.Operator):
    bl_idname = "pose.pose_snap"
    bl_label = "Simple Pose Mode Orient Snap"
    bl_options = {"REGISTER", "UNDO"}

    pose_snap_translation: bpy.props.BoolProperty(
        name="Translation",
        description="Set translation snap",
        default=True
    )

    pose_snap_rotation: bpy.props.BoolProperty(
        name="Rotation",
        description="Set rotation snap",
        default=True
    )

    pose_snap_scale: bpy.props.BoolProperty(
        name="Scale",
        description="Set scale snap",
        default=True
    )

    @classmethod
    def poll(cls, context):
        if not bpy.context.area.type == "VIEW_3D":
            return False

        sel = context.selected_pose_bones

        if sel is None:
            return False

        mode = bpy.context.active_object.mode == "POSE"
        act_bone = context.active_pose_bone in sel

        return (len(sel) > 1 and act_bone and mode)

    def execute(self, context):
        sel = context.selected_pose_bones

        act_bone = context.active_pose_bone
        sel.remove(act_bone)

        for jnt in sel:
            self.get_pre_vals(jnt)
            jnt.matrix = act_bone.matrix
            self.set_post_vals(jnt)

        return {"FINISHED"}

    def get_pre_vals(self, bone):
        loc = bone.location.copy() if not self.pose_snap_translation else None
        rot = bone.rotation_quaternion.copy() if not self.pose_snap_rotation else None
        scale = bone.scale.copy() if not self.pose_snap_scale else None

        self.pre_vals = (loc, rot, scale)

    def set_post_vals(self, bone):
        mode_case = ["location",
                     "rotation_quaternion",
                     "scale"]
        for mode, value in enumerate(self.pre_vals):
            if value is not None:
                setattr(bone, mode_case[mode], value)


def register():
    bpy.utils.register_class(Pose_Orient_Snap_OP)


def unregister():
    bpy.utils.unregister_class(Pose_Orient_Snap_OP)


if __name__ == '__main__':
    register()
