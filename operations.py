"""Module 4: Project functionality - Add, Display, Search, Update, Delete, Summary."""
import pandas as pd
from utils import (VALID_TYPES, print_header, print_table, get_int,
                   occupancy_percent, format_delay)
from data_handler import save_data


def add_record(df):
    print_header("ADD NEW TRAIN")
    train_no = get_int("Train number: ", 1)
    if train_no in df["Train_No"].values:
        print("A train with this number already exists.")
        return df
    t_type = input(f"Train type {VALID_TYPES}: ").strip().title()
    if t_type not in VALID_TYPES:
        print("Invalid train type.")
        return df
    src = input("Source: ").strip().title()
    dst = input("Destination: ").strip().title()
    total = get_int("Total seats: ", 1)
    booked = get_int("Booked seats: ", 0)
    if booked > total:
        print("Booked seats cannot exceed total seats.")
        return df
    new = {
        "Train_No": train_no, "Train_Name": f"{src}-{dst} {t_type}",
        "Train_Type": t_type, "Source": src, "Destination": dst,
        "Departure": input("Departure (HH:MM): ").strip(),
        "Arrival": input("Arrival (HH:MM): ").strip(),
        "Distance_km": get_int("Distance (km): ", 1), "Fare": get_int("Fare (Rs): ", 0),
        "Total_Seats": total, "Booked_Seats": booked,
        "Delay_Min": get_int("Delay (minutes): ", 0),
    }
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    save_data(df)
    print("Record added successfully.")
    return df


def display_all(df):
    print_header(f"ALL TRAIN RECORDS ({len(df)})")
    print_table(df)


def search_record(df):
    print_header("SEARCH TRAIN")
    key = input("Enter train number or name/station keyword: ").strip()
    if key.isdigit():
        result = df[df["Train_No"] == int(key)]
    else:
        mask = (df["Train_Name"].str.contains(key, case=False)
                | df["Source"].str.contains(key, case=False)
                | df["Destination"].str.contains(key, case=False))
        result = df[mask]
    print_table(result)
    if len(result) == 1:
        r = result.iloc[0]
        print(f"\nOccupancy: {occupancy_percent(r['Booked_Seats'], r['Total_Seats'])}% | "
              f"Delay: {format_delay(r['Delay_Min'])}")


def update_record(df):
    print_header("UPDATE TRAIN")
    train_no = get_int("Train number to update: ", 1)
    if train_no not in df["Train_No"].values:
        print("Train not found.")
        return df
    editable = ["Fare", "Total_Seats", "Booked_Seats", "Delay_Min",
                "Departure", "Arrival"]
    print("Editable fields:", editable)
    field = input("Field to update: ").strip()
    if field not in editable:
        print("Invalid field.")
        return df
    value = input("New value: ").strip()
    if field in ("Fare", "Total_Seats", "Booked_Seats", "Delay_Min"):
        if not value.isdigit():
            print("Value must be a number.")
            return df
        value = int(value)
    df.loc[df["Train_No"] == train_no, field] = value
    save_data(df)
    print("Record updated successfully.")
    print_table(df[df["Train_No"] == train_no])
    return df


def delete_record(df):
    print_header("DELETE TRAIN")
    train_no = get_int("Train number to delete: ", 1)
    if train_no not in df["Train_No"].values:
        print("Train not found.")
        return df
    if input("Are you sure? (y/n): ").strip().lower() != "y":
        print("Deletion cancelled.")
        return df
    df = df[df["Train_No"] != train_no].reset_index(drop=True)
    save_data(df)
    print("Record deleted successfully.")
    return df


def summary_report(df):
    print_header("RAILWAY SUMMARY REPORT")
    occ = df["Booked_Seats"] / df["Total_Seats"] * 100
    revenue = (df["Fare"] * df["Booked_Seats"]).sum()
    longest = df.loc[df["Distance_km"].idxmax()]
    most_delayed = df.loc[df["Delay_Min"].idxmax()]
    print(f"Total trains            : {len(df)}")
    print(f"Unique stations         : {len(set(df['Source']) | set(df['Destination']))}")
    print(f"Total seats / booked    : {df['Total_Seats'].sum()} / {df['Booked_Seats'].sum()}")
    print(f"Average occupancy       : {occ.mean():.2f}%")
    print(f"Estimated revenue       : Rs {revenue:,}")
    print(f"Average delay           : {df['Delay_Min'].mean():.1f} min")
    print(f"Longest route           : {longest['Train_Name']} ({longest['Distance_km']} km)")
    print(f"Most delayed train      : {most_delayed['Train_Name']} "
          f"({format_delay(most_delayed['Delay_Min'])})")
