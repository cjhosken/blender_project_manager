import bpy
bpm = bpy.context.scene.bpm

bpm.subdirs.clear()

subdir = bpm.subdirs.add()
subdir.name = 'abc'

subdir = bpm.subdirs.add()
subdir.name = 'audio'

subdir = bpm.subdirs.add()
subdir.name = 'backup'

subdir = bpm.subdirs.add()
subdir.name = 'comp'

subdir = bpm.subdirs.add()
subdir.name = 'desk'

subdir = bpm.subdirs.add()
subdir.name = 'flip'

subdir = bpm.subdirs.add()
subdir.name = 'geo'

subdir = bpm.subdirs.add()
subdir.name = 'hda'

subdir = bpm.subdirs.add()
subdir.name = 'render'

subdir = bpm.subdirs.add()
subdir.name = 'scripts'

subdir = bpm.subdirs.add()
subdir.name = 'sim'

subdir = bpm.subdirs.add()
subdir.name = 'tex'

subdir = bpm.subdirs.add()
subdir.name = 'video'