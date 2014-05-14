from distutils.core import setup
import py2exe
from glob import glob

data_files = [("VC90", glob(r'C:\Windows\winsxs\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91\*.*')),
            ("VC90", glob(r'C:\Windows\winsxs\Manifests\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91.manifest'))
]

setup(
    data_files=data_files,
    console=['play.py'],
    zipfile = None,
)