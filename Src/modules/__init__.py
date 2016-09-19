import os
import glob
modules = glob.glob(os.path.dirname(__file__)+"/*/api.py")
print modules
modules = [".".join(f[:-3].split('/')[-2:]) for f in modules]
for mod in modules:
    import mod.api as mod
print modules
__all__ = modules
