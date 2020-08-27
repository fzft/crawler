import os
import pkgutil
import sys
pkg_dir = os.path.dirname(__file__)
sys.path.append(pkg_dir)
for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
    exec(f'from {name} import *')