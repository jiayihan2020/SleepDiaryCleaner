import pandas as pd
import re
import sys
import platform

# --- User Input ----

working_directory = "./"
sleep_diary_csv_raw = "SIT Diary_March 23, 2022_23.40.csv"

# --------------------


def opening_sleep_diary(sleep_diary_location):
    df = pd.read_csv(sleep_diary_location, index_col=False, skiprows=1)
    df.drop(index=0, inplace=True)
    df.columns = df.columns.str.replace("\n", "")
    df.columns = df.columns.str.replace(r"Qualtrics\.Survey.*", "", regex=True)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"Subject Code (e.g. SITXXX)": "Subject"})
    df["Subject"] = df["Subject"].str.upper()
    return df


opening_sleep_diary(sleep_diary_csv_raw)


def obtaining_WT(sleep_diary_location):
    df = opening_sleep_diary(sleep_diary_location)
    df = df.filter(regex=re.compile(r"Subject|^2\.|^4\.|5\."))
    df.sort_values(by=["Subject", "4. Date at wake-time"], inplace=True)
    df.rename(
        columns={
            "4. Date at wake-time": "WTSelectedDate",
            "2. Bedtime(24 hour format, e.g. 16:35) - HH:MM": "Bedtime",
            "5. Final wake time (24 hour format, e.g. 16:35) - HH:MM": "WakeTime",
        },
        inplace=True,
    )
    df = df[["Subject", "WTSelectedDate", "Bedtime", "WakeTime"]]
    df["WTSelectedDate"] = pd.to_datetime(df["WTSelectedDate"], format="%d/%m/%Y")
    if platform.system() == "Windows":

        df["Bedtime"] = pd.to_datetime(df["Bedtime"], format="%#H:%m")
        df["Bedtime"] = pd.to_datetime(df["Bedtime"].dt.strftime("%#I:%M"))
    else:
        df["Bedtime"] = pd.to_datetime(df["Bedtime"], format="%-H:%M")
        df["Bedtime"] = pd.to_datetime(df["Bedtime"].dt.strftime("%#I:%M"))

    return df


obtaining_WT(sleep_diary_csv_raw)
