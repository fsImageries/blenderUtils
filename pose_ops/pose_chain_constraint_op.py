import bpy


class Bone_Chain_Constraint(bpy.types.Operator):
    bl_idname = "pose.bone_chain_constraint"
    bl_label = "Simple bone chain constraining automation."
    bl_options = {"REGISTER", "UNDO"}

    bone_chain_constraint__constraint_type: bpy.props.StringProperty(
        name="Constraint Type",
        description="Define which constraint should be applied.",
        default="COPY_TRANSFORMS"
    )

    bone_chain_constraint__target_suffix: bpy.props.StringProperty(
        name="Target Suffix",
        description="Define which suffix or prefix (doesn't matter) should be searched.",
        default="TGT"
    )

    bone_chain_constraint__excludes: bpy.props.StringProperty(
        name="Exclude",
        description="Define, comma seperated, joints which can be skipped. Case-sensitive, not word-length sensitive.",
        default=""
    )

    def _replacer(self, name):
        return name.replace(
            self.bone_chain_constraint__target_suffix, "")

    def _skips(self):
        stri = self.bone_chain_constraint__excludes
        return stri.split(",")

    def _create_constraint(self, src, tgt, arm):
        const = src.constraints.new(
            self.bone_chain_constraint__constraint_type)
        const.target = arm
        const.subtarget = tgt.name

    @classmethod
    def poll(cls, context):
        if not bpy.context.area.type == "VIEW_3D":
            return False

        sel = safe_selected_bones()

        if sel is None:
            return False

        mode = bpy.context.active_object.mode == "POSE"
        act_bone = context.active_pose_bone in sel

        return (len(sel) == 2 and act_bone and mode)

    def execute(self, context):

        bones = safe_selected_bones()
        act_bone = context.active_pose_bone
        bone1 = bones.pop(bones.index(act_bone))
        bone2 = bones.pop()

        childs1, childs2 = all_children(bone1), all_children(bone2)

        for src in childs1:

            if any(True for x in self._skips() if x and x.strip() in src.name):
                continue

            try:
                tgt = next(x for x in childs2 if self._replacer(
                    x.name) in src.name)
            except StopIteration:
                continue

            arm = tgt.id_data

            if src.constraints:
                isDup = False
                for const in src.constraints:
                    if (const.type == self.bone_chain_constraint__constraint_type
                            and const.target == arm and const.subtarget == tgt.name):
                        isDup = True

                if not isDup:
                    self._create_constraint(src, tgt, arm)
            else:
                self._create_constraint(src, tgt, arm)

        return {"FINISHED"}


def all_children(parent):
    top_childs = parent.children

    for child in top_childs:
        top_childs += all_children(child)

    return top_childs


def safe_selected_bones():
    return [x for x in bpy.context.active_object.pose.bones if x.bone.select]


def register():
    bpy.utils.register_class(Bone_Chain_Constraint)


def unregister():
    bpy.utils.unregister_class(Bone_Chain_Constraint)


if __name__ == '__main__':
    register()
