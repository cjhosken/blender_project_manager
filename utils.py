import bpy, os, shutil
from bpy.app.handlers import persistent

def load_presets():
    my_bundled_presets = os.path.join(os.path.dirname(os.path.realpath(__file__)), "presets")
    my_presets = os.path.join(bpy.utils.user_resource('SCRIPTS'), "presets/project_presets")

    if not os.path.isdir(my_presets):
        os.makedirs(my_presets)
        [shutil.copy2(os.path.join(my_bundled_presets, f), my_presets) for f in os.listdir(my_bundled_presets)]


def error_dialog(message = "", title = "Error", icon = 'ERROR'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def set_default_preset():
    bpm = bpy.context.scene.bpm
    if not bpm.subdirs:
        bpm.subdirs.clear()

        subdir = bpm.subdirs.add()
        subdir.name = 'assets'

        subdir = bpm.subdirs.add()
        subdir.name = 'cache'

        subdir = bpm.subdirs.add()
        subdir.name = 'output'

@persistent
def on_register(scene):
    set_default_preset()