import bpy
from bpy.types import AddonPreferences, PropertyGroup, Scene, Operator, Menu, Panel
from bl_operators.presets import AddPresetBase
from bl_ui.utils import PresetPanel
from bpy.props import *

class PREFERENCES_PT_BlenderProjectManager(AddonPreferences):
    bl_idname = __package__

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

class BlenderProjectManager_Preferences(PropertyGroup):
    auto_gen_file: BoolProperty(default=True)

class BlenderProjectManager_Subdir(PropertyGroup):
    name: StringProperty(name="", default="custom")

class BlenderProjectManager_MT_SubDir_Presets(Menu):
    bl_label = ""
    preset_subdir = "project_presets"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset

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

class BlenderProjectManager_PT_Presets(PresetPanel, Panel):
    bl_label = "Presets"
    preset_subdir = "project_presets"
    preset_operator = "script.execute_preset"
    preset_add_operator = "bpm.add_preset"



class BlenderProjectManager_Scene(PropertyGroup):
    prefs: PointerProperty(type=BlenderProjectManager_Preferences)
    subdirs: CollectionProperty(type=BlenderProjectManager_Subdir)

    @classmethod
    def register(cls):
        Scene.bpm = PointerProperty(
            name="Blender Project Manager Settings",
            description="",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        del Scene.bpm

classes = [ 
    BlenderProjectManager_Subdir, BlenderProjectManager_MT_SubDir_Presets, 
    BlenderProjectManager_OT_AddPreset, BlenderProjectManager_PT_Presets, 
    BlenderProjectManager_OT_AddSubDir, BlenderProjectManager_OT_RemoveSubDir, 
    BlenderProjectManager_Preferences, BlenderProjectManager_Scene, PREFERENCES_PT_BlenderProjectManager
]