import bpy

from bpy.props import StringProperty


class LightManager_OT_SwitchAreaSize(bpy.types.Operator):
    bl_idname = "light_manager.switch_area_size"
    bl_label = "Switch area size"

    object_name: StringProperty()

    def execute(self, context):
        light_object = bpy.data.objects[self.object_name]

        # Get size
        size_x = light_object.data.size
        size_y = light_object.data.size_y

        # Switch size
        light_object.data.size = size_y
        light_object.data.size_y = size_x

        return {'FINISHED'}
