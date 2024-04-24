bl_info = {
    "name": "Render From Each Camera",
    "blender": (2, 80, 0),
    "category": "Render",
    "description": "Render scenes from each camera and save them with incrementing names in a specified directory",
    "author": "Your Name",
    "version": (1, 0, 0),
    "location": "View3D > Sidebar > My Panel",
}

import bpy
import os

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class RENDER_OT_from_each_camera(bpy.types.Operator):
    """Render From Each Camera"""
    bl_idname = "render.from_each_camera"
    bl_label = "Render From Each Camera"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.renderpath_prop.strip() != ''

    def execute(self, context):
        base_filename = "productname"
        directory = bpy.path.abspath(context.scene.renderpath_prop)
        ensure_directory(directory)
        scene = context.scene
        original_camera = scene.camera
        file_number = 1

        for obj in scene.objects:
            if obj.type == 'CAMERA':
                scene.camera = obj
                filepath = os.path.join(directory, f"{base_filename}{file_number}.png")
                scene.render.filepath = filepath
                bpy.ops.render.render(write_still=True)
                file_number += 1

        scene.camera = original_camera
        self.report({'INFO'}, "Rendering completed.")
        return {'FINISHED'}

class RENDER_PT_custom_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Render From Each Camera"
    bl_idname = "RENDER_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My Panel'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "renderpath_prop")
        layout.operator("render.from_each_camera")

def register():
    bpy.types.Scene.renderpath_prop = bpy.props.StringProperty(
        name="Render Path",
        subtype='DIR_PATH',
        description="Directory where the renders will be saved"
    )
    bpy.utils.register_class(RENDER_OT_from_each_camera)
    bpy.utils.register_class(RENDER_PT_custom_panel)

def unregister():
    del bpy.types.Scene.renderpath_prop
    bpy.utils.unregister_class(RENDER_OT_from_each_camera)
    bpy.utils.unregister_class(RENDER_PT_custom_panel)

if __name__ == "__main__":
    register()
