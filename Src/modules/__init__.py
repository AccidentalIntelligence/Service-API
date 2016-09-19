import os
import glob
modules = glob.glob(os.path.dirname(__file__)+"/*/api.py")
print modules
__all__ = [".".join(f[:-3].split('/')[-2:]) for f in modules]
