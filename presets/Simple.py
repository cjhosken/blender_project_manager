import bpy
bpm = bpy.context.scene.bpm

bpm.subdirs.clear()

subdir = bpm.subdirs.add()
subdir.name = 'assets'

subdir = bpm.subdirs.add()
subdir.name = 'cache'

subdir = bpm.subdirs.add()
subdir.name = 'output'