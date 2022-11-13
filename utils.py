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


# This is a hack, chances of this crashing is extremely high. It would be better to request Blender to create an easier solution for this.
# https://blender.stackexchange.com/questions/13519/get-list-of-operators-in-a-menu-layout

def inject_code():
    insert_after = 'layout.operator("wm.open_mainfile"'
    insert_code = '    layout.operator("wm.project_add", text="New Project", icon="NEWFOLDER")\n'
    bpy_type = "TOPBAR_MT_file"
    bpy_type_class = getattr(bpy.types, bpy_type)

    filepath = bpy_type_class.draw.__code__.co_filename
    if filepath == "<string>":
        print("Aborting, modifications are active")
        return False
    try:
        file = open(filepath, "r")
        lines = file.readlines()
    except:
        print("%s couldn't be accessed, aborting." % filepath)
        return False

    line_start = bpy_type_class.draw.__code__.co_firstlineno - 1

    for i in range(line_start, len(lines)):
        line = lines[i]
        if not line[0].isspace() and line.lstrip()[0] not in ("#", "\n", "\r"):
            break

    line_end = i

    lines = [l[4:] for l in lines[line_start:line_end]]

    for i, line in enumerate(lines, 1):
        if insert_after in line:
            print("FOUND INSERT LINE")
            lines.insert(i, insert_code)
            break
    else:
        print("COULDN'T FIND INSERTION POINT")
        return False

    l = {}
    exec("".join(lines), {}, l)
    bpy_type_class.draw = l['draw']

    return True