#!/usr/bin/python
# -*- mode: python -*-

import os, sys
from glob import glob

resource_files = []
def add_resource_files(file_list):
    global resource_files
    for resfile in file_list:
        resource_files.append( (os.path.relpath(resfile,'../'), resfile, 'DATA') )    


### name of the executable
### depending on platform
target_location = os.path.join('dist', 'videoowl')
if sys.platform == "darwin":
    target_location = os.path.join('dist_osx', 'videoowl')
    add_resource_files( glob('../ffmpeg_osx/*') )
    add_resource_files( glob('../ffmpeg_osx/ffmpeg_presets/*') )
elif sys.platform == "win32":
    target_location = os.path.join('dist_win', 'videoowl.exe')
    add_resource_files( glob('../ffmpeg_win/*') )
    add_resource_files( glob('../ffmpeg_win/ffmpeg_presets/*') )
elif sys.platform == "linux" or sys.platform == "linux2":
    target_location = os.path.join('dist_linux', 'videoowl')
    add_resource_files( glob('../ffmpeg_linux/*') )
    add_resource_files( glob('../ffmpeg_linux/ffmpeg_presets/*') )


### build TOC
a = Analysis(['../videoowl.py'],
             pathex=[os.path.abspath(__file__)],
             hiddenimports=[],
             hookspath=None)
 

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + resource_files,
          name=target_location,
          debug=False,
          strip=None,
          upx=True,
          console=True )
   