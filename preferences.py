from bpy.types import AddonPreferences, PropertyGroup, Scene
from bpy.props import BoolProperty, PointerProperty, CollectionProperty
from .presets import BLENDERPROJECTMANAGER_PT_presets, BLENDERPROJECTMANAGER_subdir

class BLENDERPROJECTMANAGER_PT_preferences(AddonPreferences):
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
        BLENDERPROJECTMANAGER_PT_presets.draw_panel_header(row)

        # Preset folder list
        for i, subdir in enumerate(subdirs):
            row = box.row()
            row.prop(subdir, "name")
            row.operator("preferences.remove_bpm_subdir", text="", icon='X', emboss=False).index = i
        
class BLENDERPROJECTMANAGER_preferences(PropertyGroup):
    auto_gen_file: BoolProperty(default=True)

class BLENDERPROJECTMANAGER_scene(PropertyGroup):
    prefs: PointerProperty(type=BLENDERPROJECTMANAGER_preferences)
    subdirs: CollectionProperty(type=BLENDERPROJECTMANAGER_subdir)

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
    BLENDERPROJECTMANAGER_preferences, 
    BLENDERPROJECTMANAGER_scene, 
    BLENDERPROJECTMANAGER_PT_preferences
]