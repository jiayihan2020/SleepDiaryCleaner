import pandas as pd
import pyinputplus
import re
import datetime as dt


def opening_csv(filename):
    """Opens the csv in question and clean up the columns.
    Return: Pandas's dataframe
    """
    df = pd.read_csv(
        filename, encoding="cp1252", skiprows=1
    )  # Ignore first row of csv file.
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


def obtaining_WT():
    """Obtain the WT timings from each person
    Return: outputs a cleaned csv file for WT.
    """
    treated_data = opening_csv("SIT Diary_March 23, 2022_23.40.csv")
    data_interest = treated_data.filter(
        regex=re.compile(r"Subject|bedtime|^4.|^5.", re.IGNORECASE)
    )
    data_interest["WTSelectedTime"] = data_interest["4. Date at wake-time"]
    data_interest["sleep"] = (
        data_interest["1. Date at bedtime"]
        + " "
        + data_interest["2. Bedtime(24 hour format, e.g. 16:35) - HH:MM"]
    )
    data_interest["wake"] = (
        data_interest["4. Date at wake-time"]
        + " "
        + data_interest["5. Final wake time (24 hour format, e.g. 16:35) - HH:MM"]
    )
    final_data = data_interest.drop(
        columns=[
            "1. Date at bedtime",
            "2. Bedtime(24 hour format, e.g. 16:35) - HH:MM",
            "4. Date at wake-time",
            "5. Final wake time (24 hour format, e.g. 16:35) - HH:MM",
        ]
    )

    final_data.sort_values(by="Subject", inplace=True)
    strip_SIT = pyinputplus.inputStr(
        "Do you wish to change the subject code from SITXXX to SXXX (e.g SIT001 to S001)? (Y/N)"
    )
    if strip_SIT.casefold() == "y":
        final_data["Subject"] = final_data["Subject"].replace(
            to_replace=r"SIT", value="S", regex=True
        )
    print("Exporting to csv format...")
    final_data.to_csv(
        "WT_TImestamp_23_March_2022 part 2.csv", index=False, encoding="utf-8"
    )
    print("Done!")
    return None


def obtaining_BT():
    """Obtains the BT timings for each person
    Returns: output a cleaned csv file for BT."""
    treated_data = opening_csv("SIT Diary_March 23, 2022_23.40.csv")
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
    # print(data_interest["StartNap1"].apply(type))
    for column in data_interest.columns:
        if re.search(r"^Start*|End*", column):
            data_interest[column] = pd.to_datetime(data_interest[column]).dt.strftime(
                "%I:%M %p"
            )

    data_interest.to_csv("BT mine2.csv", index=False, encoding="utf-8")
    return None


def obtaining_telegram():
    """Obtain the telegram timings for each person
    Return: output a cleaned csv file for telegram timing."""
    pass


obtaining_BT()
