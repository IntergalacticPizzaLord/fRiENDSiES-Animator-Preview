import bpy

class FriendsiesAnimationPanel(bpy.types.Panel):
    bl_label = "fRiENDSiES Animation"
    bl_idname = "FRIENDSIES_PT_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'fRiENDSiES Animation'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Name and fix original armature")

        row = layout.row()
        row.operator("friendsies.rig_character")

        row = layout.row()
        row.operator("friendsies.save_pose_data")

        row = layout.row()
        row.operator("friendsies.load_pose_data")

        row = layout.row()
        row.label(text="Note: Must select an armature to save/load pose data:")

def register():
    bpy.utils.register_class(FriendsiesAnimationPanel)

def unregister():
    bpy.utils.unregister_class(FriendsiesAnimationPanel)
