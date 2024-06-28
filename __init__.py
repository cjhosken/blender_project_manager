import bpy, os
from bpy.props import StringProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
from .utils import load_presets, error_dialog, set_default_preset

from .preferences import BLENDERPROJECTMANAGER_PT_presets, classes as preferences_classes
from .presets import classes as presets_classes


bl_info = {
    "name" : "Project Manager",
    "author" : "Christopher Hosken",
    "version" : (1, 0, 0),
    "blender" : (4, 2, 0),
    "description" : "",
    "warning" : "",
    "support": "COMMUNITY",
    "doc_url": "",
    "tracker_url": "",
    "category" : "System"
}

class BLENDERPROJECTMANAGER_OT_Add(Operator):
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

class BLENDERPROJECTMANAGER_PT_browser(Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Project Settings"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator is not None and operator.bl_idname == 'WM_OT_project_add'

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

        BLENDERPROJECTMANAGER_PT_presets.draw_panel_header(row)

        for i, subdir in enumerate(subdirs):
            row = box.row()
            row.prop(subdir, "name")
            row.operator("preferences.remove_bpm_subdir", text="", icon='X', emboss=False).index = i

classes = [BLENDERPROJECTMANAGER_OT_Add, BLENDERPROJECTMANAGER_PT_browser] + presets_classes + preferences_classes

def draw(self, context):
    layout = self.layout
    layout.operator("wm.project_add", text="New Project", icon='FILE_FOLDER')

def register():
    load_presets()

    for cls in classes:
        register_class(cls)

    bpy.types.TOPBAR_MT_file.prepend(draw)

def unregister():
    for cls in classes:
        unregister_class(cls)

    bpy.types.TOPBAR_MT_file.remove(draw)

if __name__ == "__main__":
    register()
