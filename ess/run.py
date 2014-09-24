import os
import inspect
folder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
execfile(os.path.join(folder, "..", "nmpm1", "run.py"))
