# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Users/fullt/OneDrive/Рабочий стол/Python/fnaf/app.py'],
             pathex=['C:/Users/fullt/AppData/Local/Programs/Python/Python38/Lib/site-packages/panda3d'],
             binaries=[],
             datas=[('C:/Users/fullt/OneDrive/Рабочий стол/Python/fnaf/assets', 'assets/'), ('C:/Users/fullt/AppData/Local/Programs/Python/Python38/Lib/site-packages/imageio', 'imageio/'), ('C:/Users/fullt/AppData/Local/Programs/Python/Python38/Lib/site-packages/direct', 'direct/'), ('C:/Users/fullt/AppData/Local/Programs/Python/Python38/Lib/site-packages/panda3d', 'panda3d/'), ('C:/Users/fullt/AppData/Local/Programs/Python/Python38/Lib/site-packages/panda3d-1.10.11.dist-info', 'panda3d-1.10.11.dist-info/'), ('C:/Users/fullt/AppData/Local/Programs/Python/Python38/Lib/site-packages/ursina', 'ursina/'), ('C:/Users/fullt/AppData/Local/Programs/Python/Python38/Lib/site-packages/ursina-4.1.1.dist-info', 'ursina-4.1.1.dist-info/')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='FNAF 1 by lordcodes',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='C:\\Users\\fullt\\OneDrive\\Рабочий стол\\Python\\fnaf\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='FNAF 1 by lordcodes')
