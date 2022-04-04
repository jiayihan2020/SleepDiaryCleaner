import pandas as pd
import pyinputplus


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
    return df


def obtaining_WT():
    """Obtain the WT timings from each person
    Return: outputs a cleaned csv file for WT.
    """
    treated_data = opening_csv("SIT Diary_March 23, 2022_23.40.csv")

    data_interest = treated_data[
        [
            "Subject Code (e.g. SITXXX)",
            "1. Date at bedtime",
            "2. Bedtime(24 hour format, e.g. 16:35) - HH:MM",
            "4. Date at wake-time",
            "5. Final wake time (24 hour format, e.g. 16:35) - HH:MM",
        ]
    ]
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
    final_data = final_data.rename(columns={"Subject Code (e.g. SITXXX)": "Subject"})
    final_data["Subject"] = final_data["Subject"].str.upper()
    final_data.sort_values(by="Subject", inplace=True)
    strip_SIT = pyinputplus.inputStr(
        "Do you wish to change the subject code from SITXXX to SXXX (e.g SIT001 to S001)? (Y/N)"
    )
    if strip_SIT.casefold() == "y":
        final_data["Subject"] = final_data["Subject"].replace(
            to_replace=r"SIT", value="S", regex=True
        )
    print("Exporting to csv format...")
    final_data.to_csv("WT_TImestamp_23_March_2022.csv", index=False, encoding="utf-8")
    print("Done!")
    return None


def obtaining_BT():
    """Obtains the BT timings for each person
    Returns: output a cleaned csv file for BT."""
    pass


def obtaining_telegram():
    """Obtain the telegram timings for each person
    Return: output a cleaned csv file for telegram timing."""
    pass


obtaining_WT()
