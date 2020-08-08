# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['/Users/nick/personal_projects/pyqt_abf_explorer'],
             binaries=[],
             datas=[('build_app_env/lib/python3.7/site-packages/pyabf/version.txt', 'pyabf')],
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pytest', 'matplotlib'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='abf_explorer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='data/icons/traces.ico')
app = BUNDLE(exe,
             name='abf_explorer.app',
             icon='data/icons/traces.ico',
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True'}  # https://stackoverflow.com/a/40676321/6032156,
             )
