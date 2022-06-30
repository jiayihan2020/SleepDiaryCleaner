# SleepDiaryCleaner

SleepDiaryCleaner aims to extract Wake Time (WT), and Bed Time (BT) data from the raw CSV data obtained from Qualtrics with the help of the SleepAnnotate R script. The resultant CSV file can then be used for further data analysis.

- [SleepDiaryCleaner](#sleepdiarycleaner)
  - [Requirements](#requirements)
    - [Optional](#optional)
  - [Setting Up and Usage](#setting-up-and-usage)
    - [Windows](#windows)
    - [Linux and macOS](#linux-and-macos)
  - [How It Works](#how-it-works)
    - [Caveat](#caveat)

## Requirements

Ensure that you have the following software/external scripts when using this python script.

- Python 3.6+
  - Ensure that you checked the option "Add Python to PATH" during installation.
  - Pandas Library installed
- R Studio with RScript installed
- ```Step1_Cleaning modified.R``` (Adapted from SleepAnnotate Github page)
- CSV file for the sleep diary
- ```SleepDiaryCleaner.py```
- Supported Operating Systems
  - Microsoft Windows
  - Linux
  - macOS (not tested)

### Optional

- Text editor (e.g. VSCode, Sublime Text, Notepad++, etc.)

## Setting Up and Usage

Ensure that the ```SleepDiaryCleaner.py```, and ```Step1_Cleaning modified.R``` reside in the same folder as the sleep diary csv. Edit the section on the user input of `SleepDiaryCleaner.py` if necessary.

### Windows

For Windows users, you may run the `SleepDiaryCleaner.bat` file. A command prompt or Power Shell will pop up. Follow the on-screen instructions

### Linux and macOS

Launch the terminal and key in  the following command:

```bash
./SleepDiaryCleaner.py
```

Follow the on-screen instructions on the terminal.

NOTE: This is not tested on macOS. Thus, feature may ot work as intended.

## How It Works

SleepDiaryCleaner analyses the CSV file taken from the sleep diary qualtrics, and extract the relevant Sleep and Nap timings. SleepDiaryCleaner then automatically calls upon the SleepAnnotate Cleaning.R script to export the extracted data into another CSV file so that the data can be further analysed.

### Caveat

When exporting to CSV, SleepDiaryCleaner will attempt to call upon ```SleepAnnotate Cleaning.R``` . Ensure that the said R script is located in the same directory as the SleepDiaryCleaner python script. Note that this feature is only tested on Windows and Linux (Fedora). If you encounter any errors when SleepDiaryCleaner attempts to call upon ```SleepAnnotate Cleaning.R```, this could either due to:

1) An incorrect filepath was provided in the user input section of the `SleepDiaryCleaner.py`
2) RScript.exe not installed/properly, possibly due to the lack of administrative privileges on the computer.

For problem (1), ensure that the filepath is entered correctly in the `SleepDiaryCleaner.py`. For problem (2), try installing R again. If problem persists, run the R script manually using RStudio, contact your system administrator.
