"""Module 5: Data analysis using NumPy and Pandas."""
import numpy as np
import pandas as pd
from utils import print_header


def numpy_analysis(df):
    print_header("NUMPY ANALYSIS")
    fares = np.array(df["Fare"])                      # 1D array
    matrix = df[["Distance_km", "Fare", "Total_Seats", "Booked_Seats"]].head(5).to_numpy()  # 2D

    print("1D array (first 5 fares):", fares[:5])
    print("2D array shape:", matrix.shape)
    print(matrix)
    print("\nIndexing  -> matrix[0, 1] (first train fare):", matrix[0, 1])
    print("Slicing   -> fares[10:15]:", fares[10:15])
    print("Slicing   -> matrix[:3, :2] (3 trains, distance & fare):\n", matrix[:3, :2])

    print("\nFare   | Sum:", fares.sum(), "| Mean:", round(fares.mean(), 2),
          "| Max:", fares.max(), "| Min:", fares.min(), "| Std Dev:", round(fares.std(), 2))
    seats = df["Booked_Seats"].to_numpy()
    print("Booked | Sum:", seats.sum(), "| Mean:", round(seats.mean(), 2),
          "| Max:", seats.max(), "| Min:", seats.min(), "| Std Dev:", round(seats.std(), 2))
    print("Column-wise mean of 2D array:", matrix.mean(axis=0).round(2))


def pandas_analysis(df):
    print_header("PANDAS ANALYSIS")
    sample = pd.DataFrame({"Station": ["Delhi", "Mumbai", "Chennai"],
                           "Platforms": [16, 18, 17]})  # DataFrame creation
    print("Small DataFrame created from dictionary:\n", sample)

    print("\nSelected rows & columns (iloc, first 5):")
    print(df.loc[:4, ["Train_No", "Train_Name", "Fare"]].to_string(index=False))

    print("\nFiltering: Rajdhani/Shatabdi trains with delay > 30 min:")
    f = df[df["Train_Type"].isin(["Rajdhani", "Shatabdi"]) & (df["Delay_Min"] > 30)]
    print(f[["Train_No", "Train_Name", "Delay_Min"]].to_string(index=False))

    print("\nSorting: Top 5 most expensive trains:")
    print(df.sort_values("Fare", ascending=False)[["Train_Name", "Fare"]]
          .head(5).to_string(index=False))

    print("\nGroupBy Train_Type:")
    g = df.groupby("Train_Type").agg(Trains=("Train_No", "count"),
                                     Avg_Fare=("Fare", "mean"),
                                     Avg_Delay=("Delay_Min", "mean"),
                                     Total_Booked=("Booked_Seats", "sum")).round(2)
    print(g)

    print("\nStatistical analysis:")
    print(df[["Distance_km", "Fare", "Delay_Min"]].describe().round(2))


def missing_values_report(raw_df, clean_df):
    print_header("MISSING VALUE HANDLING")
    print("Missing values BEFORE cleaning:")
    print(raw_df.isnull().sum()[raw_df.isnull().sum() > 0])
    print("\nMissing values AFTER cleaning (delay=median, fare=type mean):")
    print("Total missing:", clean_df.isnull().sum().sum())


def generate_insights(df):
    print_header("KEY INSIGHTS")
    d = df.copy()
    d["Occupancy"] = (d["Booked_Seats"] / d["Total_Seats"] * 100).round(2)
    d["Revenue"] = d["Fare"] * d["Booked_Seats"]

    best = d.loc[d["Occupancy"].idxmax()]
    print(f"1. Highest occupancy: {best['Train_Name']} at {best['Occupancy']}%")

    rev = d.groupby("Train_Type")["Revenue"].sum().sort_values(ascending=False)
    print(f"2. Top revenue train type: {rev.index[0]} (Rs {rev.iloc[0]:,})")

    delay = d.groupby("Train_Type")["Delay_Min"].mean().round(1).sort_values()
    print(f"3. Most punctual type: {delay.index[0]} ({delay.iloc[0]} min avg); "
          f"least punctual: {delay.index[-1]} ({delay.iloc[-1]} min avg)")

    corr = np.corrcoef(d["Distance_km"], d["Fare"])[0, 1]
    print(f"4. Correlation between distance and fare: {corr:.2f}")

    busy = d["Source"].value_counts()
    print(f"5. Busiest origin station: {busy.index[0]} ({busy.iloc[0]} departures)")

    low = d[d["Occupancy"] < 50]
    print(f"6. {len(low)} trains run below 50% occupancy - candidates for schedule review.")

    on_time = (d["Delay_Min"] <= 10).mean() * 100
    print(f"7. On-time performance (delay <= 10 min): {on_time:.1f}%")
