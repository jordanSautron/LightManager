"""
    This module contains every addon's panels / popovers
"""

import bpy

from . import properties, preferences, operators, draw_utils


class MainPanel():
    bl_label = "Light Manager"

    def draw(self, context):
        scene_props = properties.get_props(context.scene)
        layout = self.layout
        layout.use_property_split = False

        main_lights, pinned_lights = scene_props.get_lights()

        if pinned_lights:
            pinned_col = layout.column(align=True)
            row = pinned_col.row(align=True)
            row.use_property_split = False
            row.label(text='', icon='PINNED')
            layout.separator(factor=1)

            for obj in pinned_lights:
                self.draw_light(context, obj, pinned_col)

        main_col = layout.column(align=True)
        for obj in main_lights:
            self.draw_light(context, obj, main_col)

    def draw_light(self, context, obj, layout):
        obj_props = properties.get_props(obj)

        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)

        # Select
        row.prop(
            obj_props,
            'select',
            text='',
            icon='RESTRICT_SELECT_OFF' if obj_props.select else 'RESTRICT_SELECT_ON',
            emboss=False
            )

        # Pinned
        row.prop(
            obj_props,
            'pinned',
            text='',
            icon='PINNED' if obj_props.pinned else 'UNPINNED',
            emboss=False
        )

        # Name
        name_row = row.row(align=True)
        name_row.scale_x = .8
        name_row.prop(
            obj, 
            'name', 
            text='',
            # emboss=False
            )

        # Type
        type_row = row.row(align=True)
        type_row.context_pointer_set('object', obj)
        type_row.popover(
            LIGHT_MANAGER_PT_LightData.bl_idname,
            text='',
            icon=f'LIGHT_{obj.data.type}'
        )

        # Color
        color_row = row.row(align=True)
        color_row.scale_x = .3
        color_row.prop(
            obj.data, 
            'color', 
            text=''
            )

        # Power
        power_row = row.row(align=True)
        power_row.scale_x = .7
        power_row.prop(
            obj.data, 
            'energy', 
            text=''
            )

        # Separator
        row.separator(factor=2)
        vis_row = row.row(align=True)
        vis_row.alignment = 'RIGHT'

        # Hide
        vis_row.prop(
            obj_props,
            'hide',
            icon='HIDE_ON' if obj_props.hide else 'HIDE_OFF',
            text='',
            emboss = False
        )

        # Hide render
        vis_row.prop(
            obj,
            'hide_render',
            icon='RESTRICT_RENDER_OFF',
            text='',
            emboss=False
        )


class LIGHT_MANAGER_PT_MainHeader(bpy.types.Panel, MainPanel):
    """ View3D Header popover who draw everything from MainPanel """

    bl_idname = 'LIGHT_MANAGER_PT_MainHeader'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 20

    @classmethod
    def poll(cls, context):
        return preferences.get_pref().ui_mode == 'HEADER'


class LIGHT_MANAGER_PT_MainTools(bpy.types.Panel, MainPanel):
    """ View3D UI panel (right side) who draw everything from MainPanel """

    bl_idname = 'LIGHT_MANAGER_PT_MainTools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Light Manager"

    @classmethod
    def poll(cls, context):
        return preferences.get_pref().ui_mode == 'PANEL' and context.mode == 'OBJECT'


class LIGHT_MANAGER_PT_LightData(bpy.types.Panel):
    bl_idname = 'LIGHT_MANAGER_PT_LightData'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = 'Light Type'
    bl_ui_units_x = 15

    def draw(self, context):
        layout = self.layout  
        light_obj = context.object

        # Handle object type error
        if light_obj.type != 'LIGHT':
            layout.label(text='Invalid data type', icon='ERROR')
            return

        layout.label(text='Light type:', icon=f'LIGHT_{light_obj.data.type}')
        
        # Light type
        type_row = layout.row(align=True)
        type_row.prop(
            light_obj.data,
            'type',
            text='Type',
            expand=True
        )

        # Type settings
        draw_settings = getattr(self, f'draw_{light_obj.data.type.lower()}_type', None)
        if draw_settings:
            layout.separator()
            col = layout.column(align=True)
            col.use_property_split = True
            col.use_property_decorate = False
            draw_settings(context, light_obj, col)

        # Light setting
        draw_settings = getattr(self, f'draw_{context.engine.lower()}', None)
        if draw_settings:
            col = layout.column(align=True)
            col.use_property_split = True
            col.use_property_decorate = False
            draw_settings(context, light_obj, col)
        else:
            layout.label(
                text='Unsupported Engine',
                icon='ERROR'
                )

    def draw_spot_type(self, context, obj, layout):

        # Show cone
        layout.prop(
            obj.data, 
            'show_cone', 
            text='Show Cone'
            )

        # Size
        layout.prop(
            obj.data, 
            'spot_size', 
            text='Size'
            )

        # Blend
        layout.prop(
            obj.data, 
            'spot_blend', 
            text='Blend'
            )

    def draw_area_type(self, context, obj, layout):

        # Shape
        layout.prop(
            obj.data,
            'shape',
            text='Shape'
        )

        layout.separator()

        # Size
        if obj.data.shape in {'SQUARE', 'DISK'}:
            layout.prop(
                obj.data,
                'size',
                text='Diameter' if obj.data.shape == 'DISK' else 'size'
            )
        else:
            row = layout.row(align=True)
            col = row.column(align=True)

            # Size x
            col.prop(
                obj.data,
                'size',
                text='Size X'
            )

            # Size Y
            col.prop(
                obj.data,
                'size_y',
                text='Y'
            )

            # Switch
            op = row.operator(
                operators.LightManager_OT_SwitchAreaSize.bl_idname,
                text='', 
                icon='FILE_REFRESH'
                )
            op.object_name = obj.name

    def draw_blender_eevee(self, context, obj, layout):
        light = obj.data
        props = properties.get_props(context.scene)
        obj_props = properties.get_props(obj)

        ## Basic (color & energy)
        basic_header, basic_body = draw_utils.collapsible_box(
            layout, 
            props,
            'show_basic_settings'
            )
        basic_header.label(
            text='Basics:',
            icon='LIGHT'
        )
        if basic_body:
        
            # Color
            basic_body.prop(
                light,
                'color',
                text='Color'
            )

            # Energy
            if light.type == 'SUN':
                basic_body.prop(
                    light,
                    'energy',
                    text='Strength'
                )
            else:
                # row = basic_body.row(align=True)
                basic_body.separator()
                basic_body.prop(
                    obj_props,
                    'energy',
                    text='Energy'
                )
                basic_body.prop(
                    obj_props,
                    'energy_unit',
                    text='Unit'
                )
                if obj_props.show_light_source:
                    basic_body.prop(
                        obj_props,
                        'light_source',
                        text='Source'
                    )
                basic_body.separator()

            # Specular
            basic_body.prop(
                light,
                'specular_factor',
                text='Specular'
            )

        ## Shadows
        layout.separator(factor=1)
        shadow_header, shadow_body = draw_utils.collapsible_box(
            layout, 
            props,
            'show_shadow_settings'
            )
        shadow_header.label(
            text='Shadows:',
            icon='HOLDOUT_OFF'
        )

        if shadow_body:
            # Shadow
            shadow_body.prop(
                light,
                'use_shadow',
                text='Shadow'
            )

            # Soft shadow size
            if light.type in {'POINT', 'SPOT'}:
                shadow_body.prop(
                    light,
                    'shadow_soft_size',
                    text='Soft Size'
                )

            # Sun angle
            if light.type == 'SUN':
                shadow_body.prop(
                    light,
                    'angle',
                    text='Angle (Soft Size)'
                )

            # Contact Shadow
            row = shadow_body.row(align=True)
            row.enabled = light.use_shadow
            row.prop(
                light,
                'use_contact_shadow',
                text='Contact Shadows'
            )
        
    def draw_cycles(self, context, obj, layout):
        light = obj.data
        props = properties.get_props(context.scene)

        ui_enable_rays = True
        ui_enable_shadow = True

        ## Basic (color & energy)
        basic_header, basic_body = draw_utils.collapsible_box(
            layout,
            props,
            'show_basic_settings'
            )
        basic_header.label(
            text='Basics:',
            icon='LIGHT'
        )

        if basic_body:

            # Color
            basic_body.prop(
                light,
                'color',
                text='Color'
            )

            # Energy
            basic_body.prop(
                light,
                'energy',
                text='Strength' if light.type == 'SUN' else 'Power'
            )

        ## Rays
        layout.separator(factor=1)
        rays_header, rays_body = draw_utils.collapsible_box(
            layout,
            props,
            'show_rays_settings'
            )
        rays_header.label(
            text='Rays:',
            icon='OUTLINER_DATA_LIGHTPROBE'
        )

        if rays_body:

            # Area portal
            if light.type == 'AREA':
                rays_body.prop(
                    light.cycles,
                    'is_portal',
                    text='Portal'
                )
                if light.cycles.is_portal:
                    ui_enable_rays = False
                    ui_enable_shadow = False

            # MIS
            row = rays_body.row(align=True)
            row.enabled = ui_enable_rays
            row.prop(
                light.cycles,
                'use_multiple_importance_sampling',
                text='MIS'
            )

            # Max bouces
            row = rays_body.row(align=True)
            row.enabled = ui_enable_rays
            row.prop(
                light.cycles,
                'max_bounces',
                text='Max Bounces'
            )

        ## Shadows
        layout.separator(factor=1)
        shadow_header, shadow_body = draw_utils.collapsible_box(
            layout,
            props,
            'show_shadow_settings'
        )
        shadow_header.label(
            text='Shadows:',
            icon='HOLDOUT_OFF'
        )

        if shadow_body:

            shadow_body.enabled = ui_enable_shadow


            # Shadow
            shadow_body.prop(
                light.cycles,
                'cast_shadow',
                text='Shadow'
            )

            # Soft shadow size
            if light.type in {'POINT', 'SPOT'}:
                shadow_body.prop(
                    light,
                    'shadow_soft_size',
                    text='Soft Size'
                )

            # Sun angle
            if light.type == 'SUN':
                shadow_body.prop(
                    light,
                    'angle',
                    text='Angle (Soft Size)'
                )


def extend_editor_menus(self, context):
    to_show = preferences.get_pref().ui_mode == 'HEADER'
    object_mode = context.mode == 'OBJECT'
    if to_show and object_mode:
        layout = self.layout
        layout.separator()
        layout.popover(
            LIGHT_MANAGER_PT_MainHeader.bl_idname,
            text='Lights'
        )


def register():
    bpy.types.VIEW3D_MT_editor_menus.append(extend_editor_menus)

def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(extend_editor_menus)
