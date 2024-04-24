bl_info = {
    "name": "Animate Camera To Object",
    "author": "Maher Salah",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Mahersdesigns",
    "description": "Animate camera to a selected object with depth of field",
    "category": "Camera"
}

import bpy
from mathutils import Vector

class CameraAnimateObjectOperator(bpy.types.Operator):
    """Animate camera to selected object with depth of field"""
    bl_idname = "camera.animate_to_object"
    bl_label = "Animate Camera To Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the active object
        active_object = context.active_object
        
        if active_object is None:
            self.report({'ERROR'}, "No active object selected")
            return {'CANCELLED'}
        
        # Get the camera object
        camera_object = context.scene.camera
        
        if camera_object is None:
            self.report({'ERROR'}, "No active camera selected")
            return {'CANCELLED'}
        
        # Get the start and end location for the camera
        start_location = camera_object.location
        end_location = active_object.location
        
        # Calculate the distance between the camera and the object
        distance = (end_location - start_location).length
        
        # Set the camera to the start location
        camera_object.location = start_location
        
        # Set the depth of field distance to the distance between the camera and the object
        camera_data = camera_object.data
        camera_data.dof_distance = distance
        
        # Animate the camera to the object
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
        bpy.ops.anim.keyframe_type(type='KEYFRAME')
        camera_object.location = end_location
        camera_data.dof_distance = 0.0
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
        bpy.ops.anim.keyframe_type(type='KEYFRAME')
        
        # Set the animation length to 250 frames
        context.scene.frame_end = 250
        
        return {'FINISHED'}

class CameraAnimateObjectPanel(bpy.types.Panel):
    """Creates a Panel in the Camera properties window"""
    bl_label = "Animate Camera To Object"
    bl_idname = "CAMERA_PT_animate_to_object"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Camera"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("camera.animate_to_object", text="Animate Camera To Object")

def register():
    bpy.utils.register_class(CameraAnimateObjectOperator)
    bpy.utils.register_class(CameraAnimateObjectPanel)

def unregister():
    bpy.utils.unregister_class(CameraAnimateObjectOperator)
    bpy.utils.unregister_class(CameraAnimateObjectPanel)

if __name__ == "__main__":
    register()