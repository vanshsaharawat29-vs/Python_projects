"""Module 1: Creates the railway dataset (60 records) and saves it as CSV."""
import random
import pandas as pd

STATIONS = ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru", "Hyderabad",
            "Ahmedabad", "Pune", "Jaipur", "Lucknow", "Patna", "Bhopal",
            "Nagpur", "Kanpur", "Varanasi", "Amritsar", "Guwahati", "Kochi"]

# train type -> (fare per km, average speed km/h)
TRAIN_TYPES = {"Rajdhani": (1.9, 85), "Shatabdi": (1.6, 80), "Duronto": (1.5, 75),
               "Superfast": (1.2, 60), "Express": (1.0, 50), "Passenger": (0.6, 35)}


def generate_dataset(path="railway_data.csv", n=60, seed=42):
    random.seed(seed)
    rows, used = [], set()
    for _ in range(n):
        train_no = random.randint(10000, 29999)
        while train_no in used:
            train_no = random.randint(10000, 29999)
        used.add(train_no)

        src, dst = random.sample(STATIONS, 2)
        t_type = random.choice(list(TRAIN_TYPES))
        rate, speed = TRAIN_TYPES[t_type]
        distance = random.randint(150, 2200)
        dep_min = random.randint(0, 23) * 60 + random.choice([0, 15, 30, 45])
        arr_min = (dep_min + int(distance / speed * 60)) % (24 * 60)
        total = random.choice([400, 600, 800, 1000])
        booked = random.randint(int(total * 0.35), total)

        rows.append({
            "Train_No": train_no,
            "Train_Name": f"{src}-{dst} {t_type}",
            "Train_Type": t_type,
            "Source": src,
            "Destination": dst,
            "Departure": f"{dep_min // 60:02d}:{dep_min % 60:02d}",
            "Arrival": f"{arr_min // 60:02d}:{arr_min % 60:02d}",
            "Distance_km": distance,
            "Fare": round(distance * rate),
            "Total_Seats": total,
            "Booked_Seats": booked,
            "Delay_Min": random.choice([0, 0, 5, 10, 15, 20, 30, 45, 60, 90, 120]),
        })

    df = pd.DataFrame(rows)
    # Introduce a few missing values on purpose (to demonstrate handling them)
    for idx in (4, 17, 29, 41, 55):
        df.loc[idx, "Delay_Min"] = None
    for idx in (9, 33):
        df.loc[idx, "Fare"] = None
    df.to_csv(path, index=False)
    return df


if __name__ == "__main__":
    generate_dataset()
    print("Dataset created: railway_data.csv")
