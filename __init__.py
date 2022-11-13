#  Copyright 2022 Christopher Hosken
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class

from bpy_extras.io_utils import ExportHelper

from bpy.app.handlers import persistent
import os

from .preferences import *

bl_info = {
    "name" : "Project Manager",
    "author" : "Christopher Hosken",
    "version" : (1, 0, 0),
    "blender" : (3, 2, 1),
    "description" : "",
    "warning" : "This Addon is currently under development",
    "support": "COMMUNITY",
    "doc_url": "",
    "tracker_url": "",
    "category" : "System"
}

INJECTED = False

class BlenderProjectManager_Add(bpy.types.Operator):
    bl_label = "New Project"
    bl_idname = "wm.project_add"
    bl_description = "Create a Blender project folder"

    filepath : StringProperty()
    filename : StringProperty()

    filter_glob: StringProperty(
        default="",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):

        # Create the root folder with the project name
        try:
            os.mkdir(self.filepath)
        except FileExistsError:
            error_dialog("That project already exists!", "FileExistsError")
            return {"CANCELLED"}

        # Create the subdirs

        for subdir in context.scene.bpm.subdirs:
            print(subdir.name)
            os.mkdir(os.path.join(self.filepath, subdir.name))

        # Create and open the new blender file
        if (context.scene.bpm.prefs.auto_gen_file):
            bpy.ops.wm.save_as_mainfile(filepath=os.path.join(self.filepath, self.filename.lower() + ".blend"))

        return {"FINISHED"}

    def invoke(self, context, event):
        # Open the file browser and have the user create their folder name.
        self.filepath = os.path.join(context.blend_data.filepath, "NewProject")
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}
    
    def draw(self, context):
        pass

class SubPanel(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Project Settings"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        setDefaultPresetValue()
        return operator.bl_idname == 'WM_OT_project_add'

    def draw(self, context):
        layout = self.layout

        prefs = context.scene.bpm.prefs
        subdirs = context.scene.bpm.subdirs

        row = layout.row()
        row.prop(prefs, 'auto_gen_file', text="Create .blend")

        box = layout.box()
        row = box.row()
        row.label(text="Custom Subdirectories")
        row.operator("preferences.add_bpm_subdir", text="", icon="ADD", emboss=False)

        # Add presetmanager here
        BlenderProjectManager_PT_Presets.draw_panel_header(row)

        # Preset folder list
        for i, subdir in enumerate(subdirs):
            row = box.row()
            row.prop(subdir, "name")
            row.operator("preferences.remove_bpm_subdir", text="", icon='X', emboss=False).index = i

 

# This is a hack, chances of this crashing is extremely high. It would be better to request Blender to create an easier solution for this.
# https://blender.stackexchange.com/questions/13519/get-list-of-operators-in-a-menu-layout

def inject_code():
    insert_after = 'layout.operator("wm.open_mainfile"'
    insert_code = '    layout.operator("wm.project_add", text="New Project", icon="NEWFOLDER")\n'
    bpy_type = "TOPBAR_MT_file"
    bpy_type_class = getattr(bpy.types, bpy_type)
    #module = bpy_type_class.__module__

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

    # Unindent draw func by one level, since it won't sit inside a class
    lines = [l[4:] for l in lines[line_start:line_end]]

    for i, line in enumerate(lines, 1):
        if insert_after in line:
            print("FOUND INSERT LINE")
            lines.insert(i, insert_code)
            break
    else:
        print("COULDN'T FIND INSERTION POINT")
        return False

    # Debug output
    #f = open("D:\\s.txt", "w").writelines(lines)

    l = {}
    exec("".join(lines), {}, l)
    print(l)

    #bpy_type_class.draw.__code__ = code_object # Doesn't work, since a single func is not a module

    bpy_type_class.draw = l['draw'] # exec defined our custom draw() func!

    return True


from .preferences import classes as preferences_classes
classes = [BlenderProjectManager_Add, SubPanel] + preferences_classes



def load_presets():
    import os
    import shutil

    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)

    my_bundled_presets = os.path.join(directory, "presets")

    my_presets = os.path.join(bpy.utils.user_resource('SCRIPTS'), "presets/project_presets")

    if not os.path.isdir(my_presets):
        os.makedirs(my_presets)

        files = os.listdir(my_bundled_presets)

        [shutil.copy2(os.path.join(my_bundled_presets, f), my_presets) for f in files]


def error_dialog(message = "", title = "Error!", icon = 'ERROR'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def setDefaultPresetValue():
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
def onRegister(scene):
    setDefaultPresetValue()

def register():
    global INJECTED
    load_presets()

    for cls in classes:
        register_class(cls)

    if (not INJECTED):
        INJECTED = inject_code()

    bpy.app.handlers.load_post.append(onRegister)


def unregister():
    for cls in classes:
        unregister_class(cls)