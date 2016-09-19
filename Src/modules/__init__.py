import os
import glob
modules = glob.glob(os.path.dirname(__file__)+"/*/api.py")
modules = [".".join(f[:-3].split('/')[-2:]) for f in modules]
print modules
for mod in modules:
    __import__(mod).api
