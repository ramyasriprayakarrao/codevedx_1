from pathlib import Path
from usage_manager import load_usage, add_usage, update_usage, display_usage
from prediction import predict_next_month

DATA_FILE = Path(__file__).parent / "data" / "usage_data.csv"


def get_month():
    return input("Enter month (example: Jan-2026): ").strip()


def get_units():
    while True:
        try:
            units = float(input("Enter electricity usage in units: ").strip())
            if units < 0:
                print("Usage cannot be negative. Try again.")
                continue
            return units
        except ValueError:
            print("Please enter a valid number.")


def main():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    load_usage(DATA_FILE)  # Create the CSV file if it does not exist.

    while True:
        print("\n========== UTILITY USAGE PREDICTION TOOL ==========")
        print("1. View usage records")
        print("2. Add usage record")
        print("3. Update usage record")
        print("4. Predict next month's usage")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        try:
            if choice == "1":
                display_usage(load_usage(DATA_FILE))

            elif choice == "2":
                month = get_month()
                units = get_units()
                add_usage(DATA_FILE, month, units)
                print("Record added successfully.")

            elif choice == "3":
                month = get_month()
                units = get_units()
                if update_usage(DATA_FILE, month, units):
                    print("Record updated successfully.")
                else:
                    print("Month not found. Add it as a new record instead.")

            elif choice == "4":
                records = load_usage(DATA_FILE)
                print(predict_next_month(records))

            elif choice == "5":
                print("Thank you for using the Utility Usage Prediction Tool!")
                break

            else:
                print("Invalid choice. Please select 1 to 5.")

        except (OSError, ValueError) as error:
            print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()
