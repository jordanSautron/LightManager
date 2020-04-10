import bpy
from bpy.props import EnumProperty

ADDON_NAME = __package__.split('.')[0]


class LightManagerPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME

    ui_mode: EnumProperty(
        default='HEADER',
        items=[
            ('HEADER', 'Header', 'Display addon in view 3d header'),
            ('PANEL', 'Right Panel', 'Display addon in view 3d right panel')
        ]
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text='UI display:')
        col.row(align=True).prop(
            self,
            'ui_mode',
            text='UI Display:',
            expand=True
        )


def get_pref():
    return bpy.context.preferences.addons[ADDON_NAME].preferences
