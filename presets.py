from bpy.types import Operator, Menu, Panel, PropertyGroup
from bpy.props import IntProperty, StringProperty
from bl_operators.presets import AddPresetBase
from bl_ui.utils import PresetPanel

class BLENDERPROJECTMANAGER_OT_add_preset(AddPresetBase, Operator):
    bl_idname = "bpm.add_preset"
    bl_label = "Add Preset"
    preset_menu = "BlenderProjectManager_MT_SubDir_Presets"
    preset_subdir = "project_presets"

    preset_defines = [
        "bpm = bpy.context.scene.bpm"
    ]

    preset_values = [
        "bpm.subdirs"
    ]

class BLENDERPROJECTMANAGER_OT_add_subdir(Operator):
    bl_label = "Add Subdirectory"
    bl_idname = "preferences.add_bpm_subdir"

    def execute(self, context):
        context.scene.bpm.subdirs.add()
        return {"FINISHED"}

class BLENDERPROJECTMANAGER_OT_remove_subdir(Operator):
    bl_label = "Add Subdirectory"
    bl_idname = "preferences.remove_bpm_subdir"

    index: IntProperty(default=0)

    def execute(self, context):
        context.scene.bpm.subdirs.remove(self.index)
        return {"FINISHED"}

class BLENDERPROJECTMANAGER_PT_presets(PresetPanel, Panel):
    bl_label = "Presets"
    preset_subdir = "project_presets"
    preset_operator = "script.execute_preset"
    preset_add_operator = "bpm.add_preset"

class BLENDERPROJECTMANAGER_MT_subdir_presets(Menu):
    bl_label = ""
    preset_subdir = "project_presets"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset

class BLENDERPROJECTMANAGER_subdir(PropertyGroup):
    name: StringProperty(name="", default="custom")


classes = [
    BLENDERPROJECTMANAGER_subdir, 
    BLENDERPROJECTMANAGER_OT_add_subdir,
    BLENDERPROJECTMANAGER_OT_remove_subdir,
    BLENDERPROJECTMANAGER_MT_subdir_presets,
    BLENDERPROJECTMANAGER_OT_add_preset,
    BLENDERPROJECTMANAGER_PT_presets
]