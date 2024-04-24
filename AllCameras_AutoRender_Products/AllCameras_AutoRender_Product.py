bl_info = {
    "name": "Render From Each Camera (Non-Blocking)",
    "blender": (2, 80, 0),
    "category": "Render",
    "description": "Render scenes from each camera and save them with incrementing names based on user input in a specified directory, while remaining interactive",
    "author": "Your Name",
    "version": (1, 0, 0),
    "location": "View3D > Sidebar > My Panel",
}

import bpy
import os

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def render_complete(scene, dummy):
    bpy.app.handlers.render_complete.remove(render_complete)
    bpy.ops.wm.modal_handler_finish()

class RENDER_OT_from_each_camera(bpy.types.Operator):
    """Render From Each Camera"""
    bl_idname = "render.from_each_camera"
    bl_label = "Render From Each Camera"
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None
    _cameras = []
    _index = 0
    _original_camera = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self._index < len(self._cameras):
                camera = self._cameras[self._index]
                context.scene.camera = camera
                filepath = os.path.join(self._directory, f"{self._base_filename}{self._index + 1}.png")
                context.scene.render.filepath = filepath
                bpy.ops.render.render(write_still=True)
                bpy.app.handlers.render_complete.append(render_complete)
                self._index += 1
                return {'RUNNING_MODAL'}
            else:
                context.scene.camera = self._original_camera
                self.cancel(context)
                self.report({'INFO'}, "Rendering completed.")
                return {'FINISHED'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        settings = context.scene.render_settings
        self._base_filename = settings.base_name
        self._directory = bpy.path.abspath(settings.path)
        ensure_directory(self._directory)
        self._original_camera = context.scene.camera
        self._cameras = [obj for obj in context.scene.objects if obj.type == 'CAMERA']
        self._index = 0

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    @classmethod
    def poll(cls, context):
        settings = context.scene.render_settings
        return settings.path.strip() != '' and settings.base_name.strip() != ''

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