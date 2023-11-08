import bpy
from bpy.app.handlers import persistent
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, PointerProperty, BoolVectorProperty


def get_lock_axis() -> list[bool, bool, bool]:
    # get lock axis
    axis_lock = bpy.context.scene.axis_lock
    x = axis_lock.x
    y = axis_lock.y
    z = axis_lock.z

    # if all true, set none constraint
    if (x and y and z) is True:
        return [False, ] * 3

    return [x, y, z]


def set_km_props(km, idname: str, props: str, value):
    """Set keymap properties"""
    for kmi in km.keymap_items:
        if kmi.idname == idname:
            setattr(kmi.properties, props, value)


def set_keymap(axis: list):
    """Set keymap for default and user keymap"""
    wm = bpy.context.window_manager
    axis_lock_effect = bpy.context.scene.axis_lock_effect

    keymaps_list = [
        wm.keyconfigs.default.keymaps,
        wm.keyconfigs.user.keymaps
    ]

    for keymaps in keymaps_list:
        for km in keymaps:
            # prevent from uv editor
            if axis_lock_effect.uv and km.name == "UV Editor": continue

            if axis_lock_effect.translate:
                set_km_props(km, "transform.translate", "constraint_axis", axis)
            if axis_lock_effect.rotate:
                set_km_props(km, "transform.rotate", "constraint_axis", axis)
            if axis_lock_effect.scale:
                set_km_props(km, "transform.resize", "constraint_axis", axis)


def cleanup_keymap():
    axis = [False, False, False]
    set_keymap(axis)


@persistent
def load_file_init(self, context):
    """Init keymap when load file"""
    set_keymap(get_lock_axis())


update_axis = lambda self, context: set_keymap(get_lock_axis())


class LockAxisProps(PropertyGroup):
    x: BoolProperty(name="X", default=True, update=update_axis)
    y: BoolProperty(name="Y", default=True, update=update_axis)
    z: BoolProperty(name="Z", default=True, update=update_axis)


class TransformEffectProps(PropertyGroup):
    translate: BoolProperty(name="Translate", default=True, update=update_axis)
    rotate: BoolProperty(name="Rotate", default=False, update=update_axis)
    scale: BoolProperty(name="Scale", default=False, update=update_axis)

    uv: BoolProperty(name="UV", default=False)


class AL_PT_LockAxis(bpy.types.Panel):
    bl_label = "轴向锁定"
    bl_idname = "AL_PT_LockAxis"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'

    def draw(self, context):
        layout = self.layout
        axis_lock_effect = context.scene.axis_lock_effect
        layout.use_property_split = False

        col = layout.column(align=True)
        col.prop(axis_lock_effect, "translate")
        col.prop(axis_lock_effect, "rotate")
        col.prop(axis_lock_effect, "scale")
        col.prop(axis_lock_effect, "uv")


def draw_lock_axis(self, context):
    layout = self.layout
    row = layout.row(align=True)
    # row.label(text="轴向", icon="DECORATE_LOCKED")
    axis_lock = context.scene.axis_lock
    row.scale_x = 0.8
    row.prop(axis_lock, "x", text="X", toggle=True)
    row.prop(axis_lock, "y", text="Y", toggle=True)
    row.prop(axis_lock, "z", text="Z", toggle=True)

    row.popover(panel="AL_PT_LockAxis", text="", icon="PREFERENCES")


def register():
    bpy.utils.register_class(LockAxisProps)
    bpy.utils.register_class(TransformEffectProps)
    bpy.utils.register_class(AL_PT_LockAxis)

    bpy.types.Scene.axis_lock = PointerProperty(type=LockAxisProps)
    bpy.types.Scene.axis_lock_effect = PointerProperty(type=TransformEffectProps)

    bpy.app.handlers.load_post.append(load_file_init)
    bpy.types.VIEW3D_HT_tool_header.append(draw_lock_axis)


def unregister():
    bpy.types.VIEW3D_HT_tool_header.remove(draw_lock_axis)
    bpy.app.handlers.load_post.remove(load_file_init)

    del bpy.types.Scene.axis_lock
    del bpy.types.Scene.axis_lock_effect

    bpy.utils.unregister_class(LockAxisProps)
    bpy.utils.unregister_class(TransformEffectProps)
    bpy.utils.unregister_class(AL_PT_LockAxis)

    cleanup_keymap()
