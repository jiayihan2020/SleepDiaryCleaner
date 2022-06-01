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
    pd.set_option("display.max_columns", None)

    return df


opening_sleep_diary(sleep_diary_csv_raw)


def obtaining_WT(sleep_diary_location):
    df = opening_sleep_diary(sleep_diary_location)
    search_pattern = re.compile(r"Subject|^2\.|^4\.|5\.")
    df = df.filter(regex=search_pattern)
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
        df["WTSelectedDate"] = pd.to_datetime(df["WTSelectedDate"]).dt.strftime(
            "%#d/%#m/%Y"
        )
    else:

        df["WTSelectedDate"] = pd.to_datetime(df["WTSelectedDate"]).dt.strftime(
            "%-d/%-m/%Y"
        )
    if platform.system() == "Windows":
        df["Bedtime"] = pd.to_datetime(df["Bedtime"], format="%H:%M")
        df["Bedtime"] = pd.to_datetime(df["Bedtime"]).dt.strftime("%#I:%M %p")
        df[["Bedtime", "BedtimeAMPM"]] = df["Bedtime"].str.split(" ", 1, expand=True)
        df["WakeTime"] = pd.to_datetime(df["WakeTime"], format="%H:%M")
        df["WakeTime"] = pd.to_datetime(df["WakeTime"]).dt.strftime("%#I:%M %p")
        df[["WakeTime", "WakeTimeAMPM"]] = df["WakeTime"].str.split(" ", 1, expand=True)
        df = df[
            [
                "Subject",
                "WTSelectedDate",
                "Bedtime",
                "BedtimeAMPM",
                "WakeTime",
                "WakeTimeAMPM",
            ]
        ]
        df.loc[df["Subject"].duplicated(), "Subject"] = ""
    else:
        df["Bedtime"] = pd.to_datetime(df["Bedtime"], format="%H:%M")
        df["Bedtime"] = pd.to_datetime(df["Bedtime"]).dt.strftime("%-I:%M %p")
        df[["Bedtime", "BedtimeAMPM"]] = df["Bedtime"].str.split(" ", 1, expand=True)
        df["WakeTime"] = pd.to_datetime(df["WakeTime"], format="%H:%M")
        df["WakeTime"] = pd.to_datetime(df["WakeTime"]).dt.strftime("%-I:%M %p")
        df[["WakeTime", "WakeTimeAMPM"]] = df["WakeTime"].str.split(" ", 1, expand=True)
        df = df[
            [
                "Subject",
                "WTSelectedDate",
                "Bedtime",
                "BedtimeAMPM",
                "WakeTime",
                "WakeTimeAMPM",
            ]
        ]
        df.loc[df["Subject"].duplicated(), "Subject"] = ""
    df.to_csv("./WT2.csv", index=False, encoding="utf-8")

    return None


def obtaining_BT(sleep_diary_location):
    df = opening_sleep_diary(sleep_diary_location)
    search_pattern = re.compile(r"Subject|^1\.|^7\w.")
    df = df.filter(regex=search_pattern)
    df.rename(
        columns={
            df.columns[1]: "BTSelectedDate",
            df.columns[2]: "Naps",
            df.columns[3]: "StartNap1",
            df.columns[4]: "EndNap1",
            df.columns[5]: "StartNap2",
            df.columns[6]: "EndNap2",
            df.columns[7]: "StartNap3",
            df.columns[8]: "EndNap3",
            df.columns[9]: "StartNap4",
            df.columns[10]: "EndNap4",
            df.columns[11]: "StartNap5",
            df.columns[12]: "EndNap5",
        },
        inplace=True,
    )
    df["BTSelectedDate"] = pd.to_datetime(df["BTSelectedDate"], format="%d/%m/%Y")
    if platform.system() == "Windows":
        df["BTSelectedDate"] = pd.to_datetime(df["BTSelectedDate"]).dt.strftime(
            "%#d/%#m/%Y"
        )
    else:
        df["BTSelectedDate"] = pd.to_datetime(df["BTSelectedDate"]).dt.strftime(
            "%-d/%-m/%Y"
        )
    df.sort_values(by=["Subject", "BTSelectedDate"], inplace=True)
    for col in df.columns:
        if "StartNap" in col or "EndNap" in col:
            df[col] = pd.to_datetime(df[col], format="%H:%M")
            if platform.system() == "Windows":
                df[col] = pd.to_datetime(df[col]).dt.strftime("%#I:%M %p")
            else:
                df[col] = pd.to_datetime(df[col]).dt.strftime("%-I:%M %p")
    df.loc[df["Subject"].duplicated(), "Subject"] = ""

    df.to_csv("./BT2.csv", index=False, encoding="utf-8")

    return df


obtaining_BT(sleep_diary_csv_raw)
obtaining_WT(sleep_diary_csv_raw)
