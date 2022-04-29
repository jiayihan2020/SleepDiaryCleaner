# SleepDiaryCleaner

SleepDiaryCleaner aims to extract Wake Time (WT), and Bed Time (BT) data from the raw CSV data obtained from Qualtrics with the help of the SleepAnnotate R script. The resultant CSV file can then be used for further data analysis.

- [SleepDiaryCleaner](#sleepdiarycleaner)
  - [Requirements](#requirements)
    - [Optional](#optional)
  - [Setting Up and Usage](#setting-up-and-usage)
  - [How It Works](#how-it-works)
    - [Caveat](#caveat)

## Requirements

Ensure that you have the following software/external scripts when using this python script.

- Python 3.6+
  - Ensure that you checked the option "Add Python to PATH" during installation.
- R Studio with RScript installed
- Step1_Cleaning modified.R (Adapted from SleepAnnotate Github page)
- CSV file for the sleep diary

### Optional

- Text editor (e.g. VSCode, Sublime Text, Notepad++, etc.)

## Setting Up and Usage

Ensure that the SleepDiaryCleaner.py, Sleep_diary_main.py, and Step1_Cleaning modified.R reside in the same folder as the sleep diary csv. Open Sleep_diary_main.py using Python's built-in IDLE, or a text editor. Launch the script by pressing "F5" on the keyboard if you are using IDLE. For other text editors mentioned in the [Optional](#optional) section, please consult the editor's user guide.

## How It Works

Sleep_diary_main.py: This script serves as the "user interface". User should use this script as it provides an interactive menu for ease of use, and also allows users to edit the filepath for the CSV files, and RScript.exe/RScript modules.

SleepDiaryCleaner.py: This script is the main data extractor. It is not designed for end user's usage although this script can be customised.

SleepDiaryCleaner analyses the CSV file taken from the sleep diary qualtrics, and extract the relevant Sleep and Nap timings. SleepDiaryCleaner then automatically calls upon the SleepAnnotate Cleaning.R script to export the extracted data into another CSV file so that the data can be further analysed.

### Caveat

When exporting to CSV, SleepDiaryCleaner will attempt to call upon SleepAnnotate Cleaning.R . Ensure that the said R script is located in the same directory as the SleepDiaryCleaner python script. Note that this feature is only tested on Windows. If you encounter any errors when SleepDiaryCleaner attempts to call upon SleepAnnotate Cleaning.R, you will either have to edit the filepath that points to RScript.exe/RScript located in the Sleep_diary_main.py file, or run the SleepAnnotate Cleaning.R manually using RStudio.
