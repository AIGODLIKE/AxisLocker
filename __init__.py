bl_info = {
    "name": "Axis Locker",
    "author": "AIGODLIKE社区, Atticus",
    "blender": (4, 0, 0),
    "version": (0, 1),
    "category": "AIGODLIKE",
    "support": "COMMUNITY",
    "doc_url": "",
    "tracker_url": "",
    "description": "Provide a way to lock axis in 3D View with transform tools.",
    "location": "3D View > Header",
}

__ADDON_NAME__ = __name__

from . import handle


def register():
    handle.register()


def unregister():
    handle.unregister()


if __name__ == '__main__':
    register()
