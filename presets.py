from bpy.types import Operator, Menu, Panel, PropertyGroup
from bpy.props import IntProperty, StringProperty
from bl_operators.presets import AddPresetBase
from bl_ui.utils import PresetPanel

class BlenderProjectManager_OT_AddPreset(AddPresetBase, Operator):
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

class BlenderProjectManager_OT_AddSubDir(Operator):
    bl_label = "Add Subdirectory"
    bl_idname = "preferences.add_bpm_subdir"

    def execute(self, context):
        context.scene.bpm.subdirs.add()
        return {"FINISHED"}

class BlenderProjectManager_OT_RemoveSubDir(Operator):
    bl_label = "Add Subdirectory"
    bl_idname = "preferences.remove_bpm_subdir"

    index: IntProperty(default=0)

    def execute(self, context):
        context.scene.bpm.subdirs.remove(self.index)
        return {"FINISHED"}

class BlenderProjectManager_PT_Presets(PresetPanel, Panel):
    bl_label = "Presets"
    preset_subdir = "project_presets"
    preset_operator = "script.execute_preset"
    preset_add_operator = "bpm.add_preset"

class BlenderProjectManager_MT_SubDir_Presets(Menu):
    bl_label = ""
    preset_subdir = "project_presets"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset

class BlenderProjectManager_Subdir(PropertyGroup):
    name: StringProperty(name="", default="custom")


classes = [
    BlenderProjectManager_Subdir, 
    BlenderProjectManager_OT_AddSubDir, 
    BlenderProjectManager_OT_RemoveSubDir,
    BlenderProjectManager_MT_SubDir_Presets,  
    BlenderProjectManager_OT_AddPreset,
    BlenderProjectManager_PT_Presets
]