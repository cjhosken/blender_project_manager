from bpy.types import AddonPreferences, PropertyGroup, Scene
from bpy.props import BoolProperty, PointerProperty, CollectionProperty
from .presets import BlenderProjectManager_PT_Presets, BlenderProjectManager_Subdir

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
        
class BlenderProjectManager_Preferences(PropertyGroup):
    auto_gen_file: BoolProperty(default=True)

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
    BlenderProjectManager_Preferences, 
    BlenderProjectManager_Scene, 
    PREFERENCES_PT_BlenderProjectManager
]