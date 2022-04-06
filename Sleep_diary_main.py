import pkg_resources
import sys
import subprocess
import Cleanup_and_extract as ce

try:
    import pyinputplus
except ModuleNotFoundError:
    required_packages = {"pyinputplus"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required_packages - installed
    print('pyinputplus not installed. Installing missing package...')
    launch_python = sys.executable
    subprocess.check_call([launch_python, "-m", "pip", "install", *missing])
    print('pyinputplus installed successfully.')



rscript_windows = "C:/Program Files/R/R-4.1.3/bin/Rscript.exe"  # change R-4.1.3 to the version of R you are using. You can get it from visiting the C:\Program Files\R\
rscript_linux_macOS = "usr/bin/Rscript"


####### ------ User input ------ #######

# Input working directory. The default working directory is in the folder where this python script is located.
working_directory = "./"

# Input your sleep diary filename here
sleep_diary_file_input = working_directory + "SIT Diary_March 23, 2022_23.40.csv"

####### ------ Cleaning and outputting of data ------ #######

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
if user_select == "Wake-Time Timestamp":
    print("Now obtaining Wake-TIme data...")
    ce.obtaining_WT(sleep_diary_file_input)
elif user_select == "Bed-Time Timestamp":
    if sys.platform.startswith("win32"):
        print('windows...')
        print("Now obtaining Bed-Time data...")
        ce.obtaining_BT(sleep_diary_file_input, rscript_windows)
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin')':
        user_warning = pyinputplus.inputYesNo(prompt="WARNING: Automatically calling the RScript function to generate the BT Timestamp may not work correctly! If you encountered an error, please run the Step1_Cleaning modified.R manually. Do you wish to proceed? (Y/N):\n")
        if user_warning == 'yes':
            ce.obtaining_BT(sleep_diary_file_input, rscript_linux_macOS)
        else:
            print('Please use the Step1_Cleaning modified.R manually.')
else:
    print("Now obtaining Wake-TIme data...")
    ce.obtaining_WT(sleep_diary_file_input)
    if sys.platform.startswith("win32"):
        print("Now obtaining Bed-Time data...")
        ce.obtaining_BT(sleep_diary_file_input, rscript_windows)
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        print("Now obtaining Bed-Time data...")
        ce.obtaining_BT(sleep_diary_file_input, rscript_linux_macOS)
