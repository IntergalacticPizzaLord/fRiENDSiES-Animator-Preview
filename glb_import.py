import bpy
import bpy_extras.io_utils
import os
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, Panel, PropertyGroup, WindowManager, UIList

class GLB_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False, icon_value=icon)

class GLB_OT_LoadGLB(Operator):
    bl_idname = "glb.load_glb"
    bl_label = "Load GLB"

    def execute(self, context):
        # Get the selected GLB file from the list
        selected_glb = context.window_manager.glb_list[context.window_manager.glb_list_index].name

        # Get the directory
        directory = context.scene.glb_directory

        # Create the full path to the GLB file
        path = os.path.join(directory, selected_glb)

        # Load the GLB file
        bpy.ops.import_scene.gltf(filepath=path)

        return {'FINISHED'}

    
class GLB_OT_DeleteItem(Operator):
    bl_idname = "glb.delete_item"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.window_manager.glb_list

    def execute(self, context):
        wm = context.window_manager
        list = wm.glb_list
        index = wm.glb_list_index

        list.remove(index)

        if index > 0:
            index = index - 1

        return {'FINISHED'}

class GLB_OT_MoveItem(Operator):
    bl_idname = "glb.move_item"
    bl_label = "Move an item"

    direction: bpy.props.EnumProperty(items=(('UP', "Up", ""),
                                             ('DOWN', "Down", "")))

    @classmethod
    def poll(cls, context):
        return context.window_manager.glb_list

    def move_index(self):
        index = bpy.context.window_manager.glb_list_index
        list_length = len(bpy.context.window_manager.glb_list) - 1

        new_index = index + (-1 if self.direction == 'UP' else 1)
        bpy.context.window_manager.glb_list.move(new_index, index)
        bpy.context.window_manager.glb_list_index = new_index

    def execute(self, context):
        list = context.window_manager.glb_list
        index = context.window_manager.glb_list_index

        neighbour = index + (-1 if self.direction == 'UP' else 1)
        list.move(neighbour, index)
        self.move_index()

        return {'FINISHED'}

class GLB_OT_OpenFilebrowser(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "glb.open_filebrowser"
    bl_label = "Select Folder"
    
    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        context.scene.glb_directory = self.directory

        # Clear the list
        context.window_manager.glb_list.clear()

        # Scan the directory for .glb files
        for file in os.listdir(self.directory):
            if file.endswith(".glb"):
                # Add each .glb file to the list
                item = context.window_manager.glb_list.add()
                item.name = file

        return {'FINISHED'}


class GLBPreviewerPanel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "GLB Previewer"
    bl_idname = "OBJECT_PT_glbprev"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "fRiENDSiES Animation"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.operator("glb.open_filebrowser", text="Select Folder")
        layout.template_list("GLB_UL_List", "", wm, "glb_list", wm, "glb_list_index")

        row = layout.row(align=True)
        row.operator("glb.move_item", text="", icon='TRIA_UP').direction = 'UP'
        row.operator("glb.move_item", text="", icon='TRIA_DOWN').direction = 'DOWN'
        row.operator("glb.delete_item", text="", icon='X')

        layout.operator("glb.load_glb", text="Load GLB")

class GLB_Properties(PropertyGroup):
    name: StringProperty()

def register():
    bpy.utils.register_class(GLB_UL_List)
    bpy.utils.register_class(GLB_OT_LoadGLB)
    bpy.utils.register_class(GLB_OT_DeleteItem)
    bpy.utils.register_class(GLB_OT_MoveItem)
    bpy.utils.register_class(GLB_OT_OpenFilebrowser)
    bpy.utils.register_class(GLBPreviewerPanel)
    bpy.utils.register_class(GLB_Properties)
    bpy.types.Scene.glb_directory = bpy.props.StringProperty(subtype="DIR_PATH")

    WindowManager.glb_list = CollectionProperty(type=GLB_Properties)
    WindowManager.glb_list_index = bpy.props.IntProperty(name="Index for glb_list", default=0)

def unregister():
    bpy.utils.unregister_class(GLB_UL_List)
    bpy.utils.unregister_class(GLB_OT_LoadGLB)
    bpy.utils.unregister_class(GLB_OT_DeleteItem)
    bpy.utils.unregister_class(GLB_OT_MoveItem)
    bpy.utils.unregister_class(GLB_OT_OpenFilebrowser)
    bpy.utils.unregister_class(GLBPreviewerPanel)
    bpy.utils.unregister_class(GLB_Properties)

    del bpy.types.Scene.glb_directory
    del WindowManager.glb_list
    del WindowManager.glb_list_index