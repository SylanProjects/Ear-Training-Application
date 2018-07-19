# Ear Training App
# Developed by Sylwester Stremlau
# 2018
# University of West London

import cx_Freeze

executables = [cx_freeze.Executable("main.py")]

cx_freeze.setup(
    name = "Ear Training App",
    options = {"build_exe": {"packages":["pygame"],
                            "included_files":[]}}
)
