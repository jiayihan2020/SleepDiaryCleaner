from time import sleep
import Cleanup_and_extract as ce
import pkg_resources
import sys
import subprocess

try:
    import pyinputplus
    import pandas as pd
except ModuleNotFoundError:
    print("Pandas and pyinputplus modules not found. Installing...")
    required_packages = {"pyinputplus", "pandas"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = installed - required_packages
    launch_python = sys.executable
    subprocess.call([launch_python, "-m", "pip", "install", *missing])

rscript_windows = "C:/Program Files/R/R-4.1.3/bin/Rscript.exe"  # change R-4.1.3 to the version of R you are using. You can get it from visiting the C:\Program Files\R\
rscript_linux_macOS = "usr/bin/Rscript"


####### User input #######

# Input working directory. The default working directory is in the folder where this python script is located.
working_directory = "./"

# Input your sleep diary filename here
sleep_diary_file_input = working_directory + "SIT Diary_March 23, 2022_23.40.csv"

####### Cleaning and outputing of data #######

print(
    "Hello, this script will attempt to clean up the Sleep diary csv and export to Wake time and Bedtime format."
)

user_select = pyinputplus.inputMenu(
    [
        "Wake-Time Timestamp",
        "Bed-Time Timestamp",
        "Both Wake-Time and Bed-Time Timestamp",
    ],
    numbered=True,
    prompt="Please indicate using corresponding number what kind of data you wish to extract from sleep diary:\n",
)
if user_select == "Wake-Time":
    ce.obtaining_WT(sleep_diary_file_input)
elif user_select == "Bed-Time Timestamp":
    if sys.platform.startswith("win32"):
        ce.obtaining_BT(sleep_diary_file_input, rscript_windows)
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        ce.obtaining_BT(sleep_diary_file_input, rscript_linux_macOS)
else:
    ce.obtaining_WT(ce.obtaining_WT(sleep_diary_file_input))
    if sys.platform.startswith("win32"):
        ce.obtaining_BT(sleep_diary_file_input, rscript_windows)
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        ce.obtaining_BT(sleep_diary_file_input, rscript_linux_macOS)

print("All done!")
