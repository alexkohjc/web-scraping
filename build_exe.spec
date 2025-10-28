# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Carousell Scraper
Build command: pyinstaller build_exe.spec
"""

block_cipher = None

a = Analysis(
    ['app_wrapper.py'],  # Use wrapper instead of app.py directly
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),  # Include the src folder
        ('app.py', '.'),  # Include app.py for the wrapper to run
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.scriptrunner.script_requests_handler',
        'selenium',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.firefox.service',
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
        'pandas',
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.skiplist',
        'bs4',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'numpy.distutils',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CarousellScraper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console window open to see Streamlit output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one: 'icon.ico'
)
