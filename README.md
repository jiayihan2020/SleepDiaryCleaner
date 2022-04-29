# SleepDiaryCleaner

SleepDiaryCleaner aims to extract Wake Time (WT), and Bed Time (BT) data from the raw CSV data obtained from Qualtrics with the help of the SleepAnnotate R script. The resultant CSV file can then be used for further data analysis.

- [SleepDiaryCleaner](#sleepdiarycleaner)
  - [REQUIREMENTS](#requirements)
  - [SETTING UP AND USAGE](#setting-up-and-usage)
  - [HOW IT WORKS](#how-it-works)
    - [CAVEAT](#caveat)

## REQUIREMENTS

Ensure that you have the following software/external scripts when using this python script.

- Python 3.6+
  - Ensure that you checked the option "Add Python to PATH" during installation.
- R Studio with RScript installed
- Text editor (e.g. VSCode, Sublime Text, Notepad++, etc. Python's built in text editor also works.)
- Step1_Cleaning modified.R (Adapted from SleepAnnotate Github page)
- CSV file for the sleep diary

## SETTING UP AND USAGE

Ensure that the SleepDiaryCleaner.py, main.py, and Step1_Cleaning modified.R reside in the same folder as the sleep diary csv. Open main.py using Python and run the file. To obtain the respective data, follow the on-screen instructions.

## HOW IT WORKS

SleepDiaryCleaner analyses the CSV file taken from the sleep diary qualtrics, and extract the relevant Sleep and Nap timings. SleepDiaryCleaner then automatically calls upon the SleepAnnotate Cleaning.R script to export the extracted data into another CSV file so that the data can be further analysed.

### CAVEAT

When exporting to CSV, SleepDiaryCleaner will attempt to call upon SleepAnnotate Cleaning.R . Ensure that the said R script is located in the same directory as the SleepDiaryCleaner python script. Note that this feature is only tested on Windows. If you encounter any errors when SleepDiaryCleaner attempts to call upon the RScript.exe/RScript file, you will either have to edit the filepath that points to RScript in the main.py file, or run the SleepAnnotate Cleaning.R manually using RStudio.
