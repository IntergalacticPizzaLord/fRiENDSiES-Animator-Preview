import bpy
import mathutils
import json
from bpy_extras.io_utils import ImportHelper, ExportHelper

class RigCharacterOperator(bpy.types.Operator):
    bl_idname = "friendsies.rig_character"
    bl_label = "Rig fRiENDSiE"
    bl_description = "Fix the selected fRiENDSiE rig for posing"
    fren_name: bpy.props.StringProperty(name="fRiENDSiE's Name")

    def execute(self, context):

        armatures = []
        for obj in context.scene.objects:
            if obj.type == 'ARMATURE':
                armatures.append(obj)
            elif obj.type == 'MESH':
                obj.select_set(True)
            else:
                obj.select_set(False)

        for armature in armatures[1:]:
            bpy.data.objects.remove(armature, do_unlink=True)

        armature = armatures[0] if armatures else None
        if armature:
            armature.select_set(True)
        armature.name = f"{self.fren_name}"

        for obj in context.selected_objects:
            obj.parent = None

        context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')

        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
        armature.parent = None

        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class SavePoseDataOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "friendsies.save_pose_data"
    bl_label = "Save fRiENDSiE Pose"
    bl_description = "Saves the pose data for the selected fRiENDSiE's armature"
    filename_ext = ".json"

    def execute(self, context):
        armature = context.object
        bpy.ops.object.mode_set(mode='POSE')
        pose_data = {}

        for bone in armature.pose.bones:
            pose_data[bone.name] = {
                'location': list(bone.location),
                'rotation_quaternion': list(bone.rotation_quaternion),
            }

        bpy.ops.object.mode_set(mode='OBJECT')

        with open(self.filepath, 'w') as f:
            json.dump(pose_data, f, indent=4)

        return {'FINISHED'}
    

class LoadPoseDataOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "friendsies.load_pose_data"
    bl_label = "Load fRiENDSiE Pose"
    bl_description = "Loads pose data onto the selected fRiENDSiE's armature"
    filename_ext = ".json"

    def execute(self, context):
        with open(self.filepath, 'r') as f:
            pose_data = json.load(f)

        armature = context.object
        bpy.ops.object.mode_set(mode='POSE')

        for bone in armature.pose.bones:
            if bone.name in pose_data:
                bone.location = mathutils.Vector(pose_data[bone.name]['location'])
                bone.rotation_quaternion = mathutils.Quaternion(pose_data[bone.name]['rotation_quaternion'])

        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

def register():
    bpy.utils.register_class(RigCharacterOperator)
    bpy.utils.register_class(SavePoseDataOperator)
    bpy.utils.register_class(LoadPoseDataOperator)

def unregister():
    bpy.utils.unregister_class(RigCharacterOperator)
    bpy.utils.unregister_class(SavePoseDataOperator)
    bpy.utils.unregister_class(LoadPoseDataOperator)