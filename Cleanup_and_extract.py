import datetime as dt
import re
import subprocess

import pandas as pd

pd.options.mode.chained_assignment = None


def opening_csv(filename):
    """Opens the csv in question and clean up the columns.
    Return: Pandas's dataframe
    """
    try:
        df = pd.read_csv(filename, skiprows=1)  # Ignore first row of csv file.
    except FileNotFoundError:
        print(
            "Sleep diary csv not found. Please check Sleep_diary_main.py to see if you have input the correct filepath."
        )
    pd.set_option("display.max_columns", 59)
    df.drop(index=0, inplace=True)  # Ignore the third row of the csv file
    df.columns = df.columns.str.replace("\n", "")  # Strip away unnecessary newlines
    df.columns = df.columns.str.replace(
        r"Qualtrics\.Survey.*", "", regex=True
    )  # Removes the Qualtrics gibberish using regex
    df.columns = df.columns.str.strip()  # Removes unneeded white spaces.
    df = df.rename(columns={"Subject Code (e.g. SITXXX)": "Subject"})
    df["Subject"] = df["Subject"].str.upper()
    return df


def obtaining_WT(sleep_diary_csv):
    """Obtain the WT timings from each person
    Return: outputs a cleaned csv file for WT.
    """
    treated_data = opening_csv(sleep_diary_csv)
    data_interest = treated_data.filter(
        regex=re.compile(r"Subject|bedtime|^4.|^5.", re.IGNORECASE)
    )

    data_interest["sleep"], data_interest["wake"] = [
        (
            data_interest["1. Date at bedtime"]
            + " "
            + data_interest["2. Bedtime(24 hour format, e.g. 16:35) - HH:MM"]
        ),
        (
            data_interest["4. Date at wake-time"]
            + " "
            + data_interest["5. Final wake time (24 hour format, e.g. 16:35) - HH:MM"]
        ),
    ]
    data_interest = data_interest.rename(columns={"4. Date at wake-time": "WTSelected"})
    data_interest.drop(
        columns=[
            "1. Date at bedtime",
            "2. Bedtime(24 hour format, e.g. 16:35) - HH:MM",
            "5. Final wake time (24 hour format, e.g. 16:35) - HH:MM",
        ],
        inplace=True,
    )
    data_interest.sort_values(by="Subject", inplace=True)

    data_interest.to_csv("./WT mine 2.csv", index=False, encoding="utf-8")

    return None


def obtaining_BT(sleep_diary_csv, R_Script_location):
    """Obtains the BT timings for each person
    Returns: output a cleaned csv file for BT."""
    treated_data = opening_csv(sleep_diary_csv)
    data_interest = treated_data.filter(
        regex=re.compile(r"^Subject|^1.|^7a|^7b", re.IGNORECASE)
    )
    new_column_names = ["Subject", "BTSelectedDate", "Naps"]
    tentative_list = [(f"StartNap{i}", f"EndNap{i}") for i in range(1, 6)]
    for j in tentative_list:
        for k in range(0, 2):
            new_column_names.append(j[k])
    data_interest.columns = new_column_names
    data_interest.sort_values(by="Subject", inplace=True)
    data_interest.loc[data_interest["Subject"].duplicated(), "Subject"] = ""
    cols = data_interest.columns[3:12]
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
    try:
        subprocess.call(
            [
                R_Script_location,
                "--vanilla",
                "./Step1_Cleaning modified.R",
            ]
        )
    except FileNotFoundError:
        print(
            "Either Rscript or Step1_Cleaning modified.R could not be found in the specified directory. Please check Sleep_diary_main.py for the directory input. Alternatively, you may run the Step1_Cleaning modified.R manually"
        )
    return None
