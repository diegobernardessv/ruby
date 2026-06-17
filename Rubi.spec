# -*- mode: python ; coding: utf-8 -*-
# Configuração de build do Rubi (PyInstaller 6.x) — executável único e sem console.
from PyInstaller.utils.hooks import collect_data_files

# Dados empacotados:
# - assets/ do projeto: fontes Quicksand + tema customizado rubi_theme.json
# - assets internos do CustomTkinter (temas/fontes) — sem isso o exe não abre a UI
datas = [('assets', 'assets')]
datas += collect_data_files('customtkinter')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    # tkcalendar depende de babel.numbers, que o PyInstaller não detecta sozinho
    hiddenimports=['babel.numbers'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Rubi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
