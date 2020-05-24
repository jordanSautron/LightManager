"""
    This module contains every addon's properties
"""

import bpy

from bpy.props import StringProperty, BoolProperty, PointerProperty, EnumProperty
from bpy.app.handlers import persistent

from .energy import light_sources, light_units


class LightManagerScene(bpy.types.PropertyGroup):

    # UI
    show_basic_settings = BoolProperty(default=True)
    show_rays_settings = BoolProperty()
    show_shadow_settings = BoolProperty()

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

    def light_source():
        items = [(s.type, s.name, s.description) for s in light_sources.sources]
        
        def get(self):
            value_idx = self.get('light_source', 0)
            return value_idx

        def set(self, value_idx):
            source = items[value_idx][0]
            unit = self.energy_unit
            value = self.energy
            self.id_data.data.energy = light_units.units_by_type[unit].to_watts(value, source)
            self['light_source'] = value_idx

        return locals()
    light_source: bpy.props.EnumProperty(**light_source())

    def energy_unit():
        items = [(u.type, u.name, u.description) for u in light_units.units]
        return locals()
    energy_unit: bpy.props.EnumProperty(**energy_unit())

    def energy():
        
        def get(self):
            source = self.light_source
            unit = self.energy_unit
            watts = self.id_data.data.energy
            return light_units.units_by_type[unit].from_watts(watts, source)

        def set(self, value):
            source = self.light_source
            unit = self.energy_unit
            self.id_data.data.energy = light_units.units_by_type[unit].to_watts(value, source)

        return locals()
    energy: bpy.props.FloatProperty(**energy())


def get_props(item):
    return item.LightManager


def register():
    bpy.types.Scene.LightManager = PointerProperty(type=LightManagerScene)
    bpy.types.Object.LightManager = PointerProperty(type=LightManagerObject)

def unregister():
    del bpy.types.Scene.LightManager
    del bpy.types.Object.LightManager