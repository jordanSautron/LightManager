"""
    This module contains every addon's properties
"""

import bpy

from bpy.props import StringProperty, BoolProperty, PointerProperty, EnumProperty
from bpy.app.handlers import persistent


class LightManagerScene(bpy.types.PropertyGroup):

    def get_lights(self):
        default_lights = []
        pinned_lights = []
        for obj in self.id_data.objects:
            if obj.type == 'LIGHT':
                if get_props(obj).pinned:
                    pinned_lights.append(obj)
                else:
                    default_lights.append(obj)
        return default_lights, pinned_lights

class LightManagerObject(bpy.types.PropertyGroup):
    pinned: BoolProperty()

    def select():
        
        def get(self):
            return self.id_data.select_get()

        def set(self, value):
            self.id_data.select_set(value)
            bpy.context.view_layer.objects.active = self.id_data

        return locals()
    select: BoolProperty(**select())

    def hide():
        
        def get(self):
            return self.id_data.hide_get()

        def set(self, value):
            self.id_data.hide_set(value)

        return locals()
    hide: BoolProperty(**hide())


def get_props(item):
    return item.LightManager


def register():
    bpy.types.Scene.LightManager = PointerProperty(type=LightManagerScene)
    bpy.types.Object.LightManager = PointerProperty(type=LightManagerObject)

def unregister():
    del bpy.types.Scene.LightManager
    del bpy.types.Object.LightManager