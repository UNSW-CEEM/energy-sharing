# -*- mode: python -*-

block_cipher = None

include_folders = [('application','application')]

a = Analysis(['run-dev.py'],
             pathex=['/Users/lukemarshall/Projects/energy-sharing/Flask'],
             binaries=[],
             datas=include_folders,
             hiddenimports=['engineio.async_drivers.threading','engineio','engineio.async_gevent', 'engineio.async_eventlet'],
             hookspath=['hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='run-dev',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='run-dev')
