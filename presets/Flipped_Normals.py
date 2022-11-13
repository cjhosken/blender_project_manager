import bpy
bpm = bpy.context.scene.bpm

bpm.subdirs.clear()

subdir = bpm.subdirs.add()
subdir.name = '3d'

subdir = bpm.subdirs.add()
subdir.name = 'concept'

subdir = bpm.subdirs.add()
subdir.name = 'edit'

subdir = bpm.subdirs.add()
subdir.name = 'making-of'

subdir = bpm.subdirs.add()
subdir.name = 'ref'

subdir = bpm.subdirs.add()
subdir.name = 'renderOutput'

subdir = bpm.subdirs.add()
subdir.name = 'rnd'

subdir = bpm.subdirs.add()
subdir.name = 'textures'