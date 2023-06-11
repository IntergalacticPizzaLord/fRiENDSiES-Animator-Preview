bl_info = {
    "name": "fRiENDSiES Animator",
    "author": "PizzaLord.eth",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Tool Shelf > fRiENDSiES Animation",
    "description": "Rigs, saves, and loads pose data for fRiENDSiES",
    "category": "Animation",
}

from . import operators
from . import panels
from . import glb_import

def register():
    glb_import.register()
    operators.register()
    panels.register()

def unregister():
    glb_import.unregister()
    operators.unregister()
    panels.unregister()

if __name__ == "__main__":
    register()
