bl_info = {
    "name": "Render From Each Camera",
    "blender": (2, 80, 0),
    "category": "Render",
    "description": "Render scenes from each camera and save them with incrementing names based on user input in a specified directory",
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
        settings = context.scene.render_settings
        return settings.path.strip() != '' and settings.base_name.strip() != ''

    def execute(self, context):
        settings = context.scene.render_settings
        base_filename = settings.base_name
        directory = bpy.path.abspath(settings.path)
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
        settings = context.scene.render_settings
        layout.prop(settings, "path")
        layout.prop(settings, "base_name")
        layout.operator("render.from_each_camera")

def register():
    class RenderSettings(bpy.types.PropertyGroup):
        path: bpy.props.StringProperty(
            name="Render Path",
            subtype='DIR_PATH',
            description="Directory where the renders will be saved"
        )
        base_name: bpy.props.StringProperty(
            name="Base Filename",
            description="Base filename for rendered images"
        )
    
    bpy.utils.register_class(RenderSettings)
    bpy.types.Scene.render_settings = bpy.props.PointerProperty(type=RenderSettings)
    bpy.utils.register_class(RENDER_OT_from_each_camera)
    bpy.utils.register_class(RENDER_PT_custom_panel)

def unregister():
    del bpy.types.Scene.render_settings
    bpy.utils.unregister_class(RenderSettings)
    bpy.utils.unregister_class(RENDER_OT_from_each_camera)
    bpy.utils.unregister_class(RENDER_PT_custom_panel)

if __name__ == "__main__":
    register()
