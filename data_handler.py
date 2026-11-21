"""Module 3: File handling - reading, cleaning and saving the dataset."""
import os
import pandas as pd

DATA_FILE = "railway_data.csv"


def read_raw_file(path=DATA_FILE, lines=3):
    """Read the CSV with plain Python file handling and show a preview."""
    with open(path, "r") as f:
        content = f.readlines()
    print(f"File '{path}' has {len(content) - 1} data rows. Preview:")
    for line in content[:lines]:
        print("  ", line.strip())


def load_data(path=DATA_FILE):
    """Load the dataset using Pandas (creates it first if missing)."""
    if not os.path.exists(path):
        from generate_dataset import generate_dataset
        generate_dataset(path)
    return pd.read_csv(path)


def clean_data(df):
    """Handle missing values: delay -> median, fare -> mean of same train type."""
    df = df.copy()
    df["Delay_Min"] = df["Delay_Min"].fillna(df["Delay_Min"].median())
    df["Fare"] = df["Fare"].fillna(df.groupby("Train_Type")["Fare"].transform("mean"))
    df["Fare"] = df["Fare"].round().astype(int)
    df["Delay_Min"] = df["Delay_Min"].astype(int)
    return df


def save_data(df, path=DATA_FILE):
    """Write the DataFrame back to the CSV file."""
    df.to_csv(path, index=False)
