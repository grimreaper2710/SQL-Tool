import sys
from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["jinja2","os","sys","time","requests","urllib","xml","base64","csv","flask","xml2xlsx","openpyxl","datetime"] # <-- Include easy_gui
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Cloud SQL Tool",
        version = "0.1",
        description = "Browser based tool to execute sql queries and download sql dumps!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Cloud SQL Tool.py",icon='SQL_Tool.ico')])
