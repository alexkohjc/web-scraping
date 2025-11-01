# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Carousell Scraper
Build command: pyinstaller build_exe.spec
"""

import os
import sys

block_cipher = None

# Collect Streamlit data files
def get_streamlit_datas():
    """Collect Streamlit's static files"""
    datas = []
    try:
        import streamlit
        streamlit_path = os.path.dirname(streamlit.__file__)

        # Add static files (required for web interface)
        static_path = os.path.join(streamlit_path, 'static')
        if os.path.exists(static_path):
            datas.append((static_path, 'streamlit/static'))

        # Add runtime files
        runtime_path = os.path.join(streamlit_path, 'runtime')
        if os.path.exists(runtime_path):
            datas.append((runtime_path, 'streamlit/runtime'))

        # Add vendor files if they exist
        vendor_path = os.path.join(streamlit_path, 'vendor')
        if os.path.exists(vendor_path):
            datas.append((vendor_path, 'streamlit/vendor'))

        print(f"[OK] Collected Streamlit files from: {streamlit_path}")
    except ImportError:
        print("[WARNING] Could not collect Streamlit files. Make sure streamlit is installed.")

    return datas

streamlit_datas = get_streamlit_datas()

a = Analysis(
    ['app_wrapper.py'],  # Use wrapper instead of app.py directly
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),  # Include the src folder
        ('app.py', '.'),  # Include app.py for the wrapper to run
        ('.streamlit', '.streamlit'),  # Include Streamlit config
    ] + streamlit_datas,  # Add Streamlit static files
    hiddenimports=[
        'streamlit',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.scriptrunner.script_requests_handler',
        'streamlit.web.cli',
        'streamlit.web.bootstrap',
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.state',
        'streamlit.components.v1',
        'watchdog',
        'watchdog.observers',
        'watchdog.events',
        'click',
        'tornado',
        'altair',
        'validators',
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
    runtime_hooks=['fix_streamlit_hook.py'],  # Fix Streamlit metadata issue
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
