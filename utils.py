"""Module 2: Helper (user-defined) functions and Python data structure demos."""

# Tuple: fixed set of valid train types (immutable)
VALID_TYPES = ("Rajdhani", "Shatabdi", "Duronto", "Superfast", "Express", "Passenger")


def print_header(title):
    """User-defined function 1: print a formatted heading."""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def print_table(df):
    """User-defined function 2: print a DataFrame neatly."""
    if df.empty:
        print("No records to display.")
    else:
        print(df.to_string(index=False))


def get_int(prompt, minimum=0):
    """User-defined function 3: keep asking until a valid integer is entered."""
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
            print(f"  Value must be at least {minimum}.")
        except ValueError:
            print("  Please enter a valid whole number.")


def occupancy_percent(booked, total):
    """User-defined function 4: seat occupancy percentage."""
    return round(booked / total * 100, 2) if total else 0.0


def format_delay(minutes):
    """User-defined function 5: convert minutes to 'Xh Ym' text."""
    minutes = int(minutes)
    return f"{minutes // 60}h {minutes % 60}m" if minutes >= 60 else f"{minutes}m"


def data_structures_demo(df):
    """Demonstrates List, Tuple, Set, Dictionary, List & Dictionary methods."""
    print_header("PYTHON DATA STRUCTURES DEMO")

    # 1. LIST + list methods
    columns = list(df.columns)
    columns.append("Occupancy_%")
    columns.sort()
    print("1. List (append, sort):", columns[:5], "...")

    # 2. TUPLE
    print("2. Tuple of valid train types:", VALID_TYPES)

    # 3. SET (unique values)
    stations = set(df["Source"]) | set(df["Destination"])
    print(f"3. Set -> {len(stations)} unique stations:", sorted(stations))

    # 4. DICTIONARY
    type_count = {}
    for t in df["Train_Type"]:
        type_count[t] = type_count.get(t, 0) + 1
    print("4. Dictionary (trains per type):", type_count)

    # 5. DICTIONARY METHODS (items, keys, values, update)
    type_count.update({"Metro": 0})
    busiest = max(type_count.items(), key=lambda kv: kv[1])
    print("5. Dict methods -> keys:", list(type_count.keys()))
    print("   values:", list(type_count.values()), "| most common type:", busiest)
