import csv
from pathlib import Path

FIELDNAMES = ["month", "units"]


def load_usage(file_path):
    """Read usage records from CSV. Create an empty CSV if needed."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

    records = []
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                records.append({
                    "month": row["month"].strip(),
                    "units": float(row["units"])
                })
            except (KeyError, TypeError, ValueError):
                # Ignore incomplete or invalid rows instead of crashing.
                continue
    return records


def save_usage(file_path, records):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for record in records:
            writer.writerow({
                "month": record["month"],
                "units": record["units"]
            })


def add_usage(file_path, month, units):
    if not month:
        raise ValueError("Month cannot be empty.")
    if units < 0:
        raise ValueError("Usage cannot be negative.")

    records = load_usage(file_path)
    if any(item["month"].lower() == month.lower() for item in records):
        raise ValueError("A record for this month already exists. Use Update instead.")

    records.append({"month": month, "units": float(units)})
    save_usage(file_path, records)


def update_usage(file_path, month, units):
    if not month:
        raise ValueError("Month cannot be empty.")
    if units < 0:
        raise ValueError("Usage cannot be negative.")

    records = load_usage(file_path)
    for record in records:
        if record["month"].lower() == month.lower():
            record["units"] = float(units)
            save_usage(file_path, records)
            return True
    return False


def display_usage(records):
    if not records:
        print("No usage records found. Add some records first.")
        return

    print("\n----------- SAVED USAGE RECORDS -----------")
    print(f"{'Month':<18} {'Units':>10}")
    print("-" * 30)
    for record in records:
        print(f"{record['month']:<18} {record['units']:>10.2f}")
    print("-" * 30)
