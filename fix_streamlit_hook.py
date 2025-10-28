"""
PyInstaller runtime hook to fix Streamlit metadata issue
This file will be executed before the app starts when bundled
"""
import sys
import os

# Fix for Streamlit's version detection in PyInstaller
if getattr(sys, 'frozen', False):
    # We're running in a bundle
    import importlib.metadata

    # Mock the streamlit package metadata
    class MockDistribution:
        def __init__(self, version):
            self._version = version

        @property
        def version(self):
            return self._version

        @property
        def metadata(self):
            return {"Version": self._version}

    # Store original functions
    _original_distribution = importlib.metadata.distribution
    _original_version = importlib.metadata.version

    def patched_distribution(distribution_name):
        if distribution_name.lower() == 'streamlit':
            return MockDistribution('1.28.0')
        return _original_distribution(distribution_name)

    def patched_version(distribution_name):
        if distribution_name.lower() == 'streamlit':
            return '1.28.0'
        return _original_version(distribution_name)

    # Patch the functions
    importlib.metadata.distribution = patched_distribution
    importlib.metadata.version = patched_version
