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

def register():
    operators.register()
    panels.register()

def unregister():
    operators.unregister()
    panels.unregister()

if __name__ == "__main__":
    register()
