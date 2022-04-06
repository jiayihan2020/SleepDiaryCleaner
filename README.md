# SleepDiaryCleaner

SleepDiaryCleaner aims to extract Wake Time (WT), and Bed Time (BT) data from the raw CSV data obtained from Qualtrics. SleepDiaryCleaner will then export the extracted data to their respective suitable CSV files for further data analysis.

- [SleepDiaryCleaner](#sleepdiarycleaner)
  - [PREREQUISITES](#prerequisites)
  - [SETTING UP AND USAGE](#setting-up-and-usage)
  - [DATA EXTRACTION](#data-extraction)
    - [Extracting WT Data](#extracting-wt-data)
    - [Extracting BT Data](#extracting-bt-data)

---

## PREREQUISITES

Ensure that you have the following software/external scripts when using this python script.

- Python 3.6+
  - Ensure that you checked the option "Add Python to PATH" during installation.
- R Studio with RScript installed
- Text editor (e.g. VSCode, Sublime Text, Notepad++, etc. Python's built in text editor also works.)
- Step1_Cleaning modified.R (Adapted from SleepAnnotate Github page)
- CSV file for the sleep diary

## SETTING UP AND USAGE

Ensure that the SleepDiaryCleaner.py, main.py, and Step1_Cleaning modified.R reside in the same folder as the sleep diary csv. Open main.py using Python and run the file. To obtain the respective data, follow the onscreen instructions.

## DATA EXTRACTION

### Extracting WT Data

The WT data extraction works out of the box. Simply enter your choice indicated by the onscreen instruction and the formatted file will be exported in the same directory.

### Extracting BT Data

The BT extractor can only export BT Timestamped csv file with the help of the Step1_Cleaning modified.R script.
