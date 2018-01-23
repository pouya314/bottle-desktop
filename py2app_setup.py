import sys
import os
from setuptools import setup
 
 
def tree(src):
    return [(root, map(lambda f: os.path.join(root, f), files)) for (root, dirs, files) in os.walk(os.path.normpath(src))]
 
 
ENTRY_POINT = ['cdp.py']
 
DATA_FILES = tree('views') + tree('static/img') + tree('static/css') + tree('static/js')
OPTIONS = {'argv_emulation': False,
           'strip': True,
           # 'iconfile': 'icon.icns',
           'includes': ['WebKit', 'Foundation', 'webview']}
 
setup(
    app=ENTRY_POINT,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=[
        'py2app',
        'bottle',
        'pywebview[cocoa]',
    ],
)
