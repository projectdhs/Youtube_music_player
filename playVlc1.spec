# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['playVlc.py'],
             pathex=['D:\\py'],
             binaries=[],
             datas=[('./libvlc.dll', '.'), ('./axvlc.dll', '.'), ('./libvlccore.dll', '.'), ('./npvlc.dll', '.'), ( "D:/py/image/*.*", ".")],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += Tree('C:\Program Files\VideoLAN\VLC\plugins', prefix='plugins')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
		  icon='D:/py/image/player.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='playVlc')
