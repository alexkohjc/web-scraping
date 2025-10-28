"""
Helper script to collect Streamlit data files for PyInstaller
Run this to generate the correct datas list
"""
import os
import sys

def get_streamlit_datas():
    """Get the correct datas list for Streamlit"""
    try:
        import streamlit
        streamlit_path = os.path.dirname(streamlit.__file__)

        datas = []

        # Add static files
        static_path = os.path.join(streamlit_path, 'static')
        if os.path.exists(static_path):
            datas.append((static_path, 'streamlit/static'))
            print(f"Found: {static_path}")

        # Add runtime files
        runtime_path = os.path.join(streamlit_path, 'runtime')
        if os.path.exists(runtime_path):
            datas.append((runtime_path, 'streamlit/runtime'))
            print(f"Found: {runtime_path}")

        # Add vendor files
        vendor_path = os.path.join(streamlit_path, 'vendor')
        if os.path.exists(vendor_path):
            datas.append((vendor_path, 'streamlit/vendor'))
            print(f"Found: {vendor_path}")

        print("\nAdd this to your .spec file datas section:")
        print("    datas=[")
        print("        ('src', 'src'),")
        print("        ('app.py', '.'),")
        for src, dst in datas:
            print(f"        (r'{src}', '{dst}'),")
        print("    ],")

        return datas
    except ImportError:
        print("ERROR: Streamlit not installed!")
        print("Run: pip install streamlit")
        return []

if __name__ == '__main__':
    get_streamlit_datas()
