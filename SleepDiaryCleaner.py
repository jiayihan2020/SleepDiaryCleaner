import re
import subprocess
import sys

try:
    import pandas as pd
except ModuleNotFoundError:
    print("pandas package not found! Installing pandas...")
    missing = {"pandas"}
    launch_python = sys.executable
    subprocess.check_call([launch_python, "-m", "pip", "install", *missing])
    print(
        "Missing package installed. It is recommended to restart python to apply the updates to the local Python library."
    )
else:
    pd.options.mode.chained_assignment = None


def opening_csv(filename):
    """Opens the csv in question and clean up the columns.
    Return: Pandas's dataframe
    """
    try:
        # Open the Sleep diary csv and ignore first row of csv file.
        df = pd.read_csv(filename, skiprows=1)
    except FileNotFoundError:
        print(
            "Sleep diary csv not found. Please check Sleep_diary_main.py to see if you have input the correct filepath."
        )
    else:
        pd.set_option("display.max_columns", 59)
        # Ignore the third row of the csv file
        df.drop(index=0, inplace=True)
        # Strip away unnecessary newlines
        df.columns = df.columns.str.replace("\n", "")
        # Removes the Qualtrics gibberish using regex
        df.columns = df.columns.str.replace(r"Qualtrics\.Survey.*", "", regex=True)
        # Removes unneeded white spaces.
        df.columns = df.columns.str.strip()
        # Rename Subject heading
        df = df.rename(columns={"Subject Code (e.g. SITXXX)": "Subject"})
        # Standardise sit to SIT
        df["Subject"] = df["Subject"].str.upper()
    return df


def obtaining_WT(sleep_diary_csv):
    """Obtain the WT timings from each person
    Return: outputs a cleaned csv file for WT.
    """
    print("Opening file...")
    treated_data = opening_csv(sleep_diary_csv)
    # Filter unneeded columns using regex
    data_interest = treated_data.filter(
        regex=re.compile(r"Subject|^2.|^4.|^5.", re.IGNORECASE)
    )
    data_interest["BedtimeAMPM"] = data_interest[
        "2. Bedtime(24 hour format, e.g. 16:35) - HH:MM"
    ]
    data_interest["WakeTimeAMPM"] = data_interest[
        "5. Final wake time (24 hour format, e.g. 16:35) - HH:MM"
    ]
    data_interest["BedtimeAMPM"].apply(pd.to_datetime)
    data_interest["WakeTimeAMPM"].apply(pd.to_datetime)
    data_interest["BedtimeAMPM"] = pd.to_datetime(
        data_interest["BedtimeAMPM"]
    ).dt.strftime("%p")
    data_interest["WakeTimeAMPM"] = pd.to_datetime(
        data_interest["WakeTimeAMPM"]
    ).dt.strftime("%p")

    data_interest.rename(
        columns={
            "4. Date at wake-time": "WTSelectedDate",
            "2. Bedtime(24 hour format, e.g. 16:35) - HH:MM": "Bedtime",
            "5. Final wake time (24 hour format, e.g. 16:35) - HH:MM": "WakeTime",
        },
        inplace=True,
    )
    data_interest["Bedtime"].apply(pd.to_datetime)
    data_interest["Bedtime"] = pd.to_datetime(data_interest["Bedtime"]).dt.strftime(
        "%I:%M"
    )
    data_interest["WakeTime"].apply(pd.to_datetime)
    data_interest["WakeTime"] = pd.to_datetime(data_interest["Bedtime"]).dt.strftime(
        "%I:%M"
    )

    data_interest = data_interest[
        [
            "Subject",
            "WTSelectedDate",
            "Bedtime",
            "BedtimeAMPM",
            "WakeTime",
            "WakeTimeAMPM",
        ]
    ]
    data_interest.sort_values(by="Subject", inplace=True)
    print("Waketime data generated. Exporting to CSV...")

    data_interest.to_csv("./WT mine 2.csv", index=False, encoding="utf-8")

    return None


def obtaining_BT(sleep_diary_csv):
    """Obtains the BT timings for each person
    Returns: output a cleaned csv file for BT."""
    print("Opening Sleep diary csv...")
    treated_data = opening_csv(sleep_diary_csv)
    # filter unneeded columns using regex
    print("Analysing")
    data_interest = treated_data.filter(
        regex=re.compile(r"^Subject|^1.|^7a|^7b", re.IGNORECASE)
    )
    # Creating and renaming column headers
    new_column_names = ["Subject", "BTSelectedDate", "Naps"]
    tentative_list = [(f"StartNap{i}", f"EndNap{i}") for i in range(1, 6)]
    for j in tentative_list:
        for k in range(0, 2):
            new_column_names.append(j[k])
    data_interest.columns = new_column_names

    # Sort dataframe by Subject column
    data_interest.sort_values(by="Subject", inplace=True)
    # Remove duplicate Subject Code and replace with ""
    data_interest.loc[data_interest["Subject"].duplicated(), "Subject"] = ""
    cols = data_interest.columns[3:12]

    # Format the datetime to 12 hour format.
    data_interest[cols] = data_interest[cols].apply(pd.to_datetime, format="%H:%M%S")
    for column in data_interest.columns:
        if re.search(r"^Start*|End*", column):
            data_interest[column] = pd.to_datetime(data_interest[column]).dt.strftime(
                "%I:%M %p"
            )

    data_interest.to_csv(
        "./BT mine2.csv",
        index=False,
        encoding="utf-8",
    )
    print("Bed Time raw data obtained. Exporting to csv...")

    return None


def calling_RScript(R_cleaning_script, *args):
    print("Calling R Script to further format resulting csv...")
    error_message = "Either Rscript or Step1_Cleaning modified.R could not be found in the specified directory. Please check Sleep_diary_main.py for the directory input or check if Rstudio is installed. Alternatively, you may run the Step1_Cleaning modified.R manually using RStudio."
    if sys.platform.startswith("win32"):
        try:
            subprocess.run(
                [
                    args[0],
                    "--vanilla",
                    R_cleaning_script,
                ]
            )
        except FileNotFoundError:
            print(error_message)
        else:
            print("Done!")
    elif sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
        try:
            subprocess.run(
                [
                    args[1],
                    "--vanilla",
                    R_cleaning_script,
                ]
            )
        except FileNotFoundError:
            print(error_message)
        else:
            print("Done!")
    else:
        print(
            "Unknown operating system detected. Please run the R script manually to clean the file."
        )
    return None
