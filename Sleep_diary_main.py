import pkg_resources
import sys
import subprocess
import SleepDiaryCleaner as ce

try:
    import pyinputplus
except ModuleNotFoundError:
    required_packages = {"pyinputplus"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required_packages - installed
    print("pyinputplus not installed. Installing missing package...")
    launch_python = sys.executable
    subprocess.check_call([launch_python, "-m", "pip", "install", *missing])
    print(
        "pyinputplus installed successfully. It is recommended to restart Python to apply the update to the local Python package library."
    )


####### ------ User input ------ #######

rscript_windows = "C:/Program Files/R/R-4.1.3/bin/Rscript.exe"  # change R-4.1.3 to the version of R you are using. You can get it from visiting the C:\Program Files\R\

rscript_linux_macOS = "usr/bin/Rscript"

# Input working directory. The default working directory is in the folder where this python script is located.
working_directory = "./"

# Input your sleep diary filename here
sleep_diary_file_input = working_directory + "SIT Diary_March 23, 2022_23.40 modded.csv"

# Input the location for the Step1_Cleaning modified.R script
R_csv_cleaning = "Step1_Cleaning modified.R"


####### ------ Cleaning and outputting of data ------ #######

print(
    "Hello, this script will attempt to clean up the Sleep diary csv and export to Wake time and Bedtime format.\n"
)

auto_launch_R_cleaning = pyinputplus.inputYesNo(
    prompt="Do you want to call upon Step1_Cleaning modified.R automatically to clean the csv to the desired csv format that is suitable for further analysis (Y/N)?\n"
)


ce.obtaining_WT(sleep_diary_file_input)
ce.obtaining_BT(sleep_diary_file_input)
if auto_launch_R_cleaning:
    ce.calling_RScript(R_csv_cleaning, rscript_windows, rscript_linux_macOS)
