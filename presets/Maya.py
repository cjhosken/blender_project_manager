import bpy
bpm = bpy.context.scene.bpm

bpm.subdirs.clear()

subdir = bpm.subdirs.add()
subdir.name = 'scenes'

subdir = bpm.subdirs.add()
subdir.name = 'sourceimages'

subdir = bpm.subdirs.add()
subdir.name = 'movies'

subdir = bpm.subdirs.add()
subdir.name = 'image'