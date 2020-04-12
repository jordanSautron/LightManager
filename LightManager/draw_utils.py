"""
    This module contains tool for drawing on UI layout
"""


def collapsible_box(layout, show_prop_id, show_prop_name):
    """
        Create a colapsible box with a header part and a body part.
        The body part will be visible only if show_prop in True

         ______________________________________________________
        |  >   Header (for title)                              |
        |______________________________________________________|
        |                                                      |
        |      Body for contents                               |
        |                                                      |
        |______________________________________________________|

        :param  layout: Layout to draw into
        :type   layout: bpy.types.UILayout

        :param  show_prop_id: object who contains the show property used to control body visibility
        :type   show_prop_id: bpy.types.PropertyGroup

        :param  show_prop_name: Attribute name of the show_prop_id object use to control body visibility
        :type   show_prop_name: str()

        :return: header_layout, body_layout
    """
    
    col = layout.column(align=True)

    # Header
    box = col.box()
    row = box.row(align=True)
    row.use_property_split = False
    row.prop(
        show_prop_id,
        show_prop_name,
        text='',
        icon='TRIA_DOWN' if getattr(show_prop_id, show_prop_name) else 'TRIA_RIGHT',
        emboss=False
    )
    header_row = row.row(align=True)

    # Body
    body = None
    if getattr(show_prop_id, show_prop_name):
        box = col.box()
        body = box.column(align=True)

    return header_row, body
