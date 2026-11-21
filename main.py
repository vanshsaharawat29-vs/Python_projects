"""Railway Management System - main program (menu driven)."""
from data_handler import load_data, clean_data, read_raw_file, save_data
from operations import (add_record, display_all, search_record,
                        update_record, delete_record, summary_report)
from analysis import (numpy_analysis, pandas_analysis,
                      missing_values_report, generate_insights)
from utils import print_header, data_structures_demo

MENU = """
1. Display all records        6. Summary report
2. Add new record             7. NumPy analysis
3. Search record              8. Pandas analysis
4. Update record              9. Insights
5. Delete record             10. Python data structures demo
0. Exit
"""


def main():
    print_header("RAILWAY MANAGEMENT SYSTEM")
    df = load_data()
    read_raw_file()
    raw = df.copy()
    df = clean_data(df)
    save_data(df)
    missing_values_report(raw, df)

    actions = {"1": display_all, "3": search_record, "6": summary_report,
               "7": numpy_analysis, "8": pandas_analysis, "9": generate_insights,
               "10": data_structures_demo}
    modifiers = {"2": add_record, "4": update_record, "5": delete_record}

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Thank you for using the Railway Management System!")
            break
        elif choice in actions:
            actions[choice](df)
        elif choice in modifiers:
            df = modifiers[choice](df)
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
