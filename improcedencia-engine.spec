# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

BASE_DIR = Path('.').resolve()

a = Analysis(
    ['scripts/improcedencia.py'],
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=[
        ('normas/*', 'normas'),
        ('docs/*', 'docs'),
        ('plantillas_maestras/*.docx', 'plantillas_maestras'),
    ],
    hiddenimports=[
        'docx',
        'openpyxl',
        'src',
        'src.builder',
        'src.config',
        'src.improcedencia_engine',
        'src.rules_engine',
        'scripts',
        'scripts.guardia_improcedencia',
        'scripts.verificar_improcedencia',
    ],
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
    name='improcedencia-engine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
