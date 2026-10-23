"""Создать копию сессий с 12% пропусков в трёх столбцах длительности."""

import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/raw/online_shoppers_intention.csv"
OUTPUT = ROOT / "data/processed/online_shoppers_incomplete.csv"
COLUMNS = [
    "Administrative_Duration",
    "Informational_Duration",
    "ProductRelated_Duration",
]
SEED = 42
MISSING_RATE = 0.12


def main():
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        fields = reader.fieldnames
    rng = random.Random(SEED)
    count = round(len(rows) * MISSING_RATE)
    for column in COLUMNS:
        for index in rng.sample(range(len(rows)), count):
            rows[index][column] = ""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Создано {len(rows)} строк; по {count} пропусков в каждом из трёх столбцов.")


if __name__ == "__main__":
    main()
