"""Скрыть 20% известных значений в трёх числовых признаках домов."""

import csv
import random
from itertools import dropwhile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/raw/housing_prices.csv"
OUTPUT = ROOT / "data/processed/housing_prices_incomplete.csv"
COLUMNS = ["LotArea", "GrLivArea", "TotalBsmtSF"]
SEED = 42


def main():
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(dropwhile(lambda line: not line.strip(), stream))
        rows = list(reader)
        fields = reader.fieldnames
    rng = random.Random(SEED)
    for column in COLUMNS:
        observed = [index for index, row in enumerate(rows) if row[column] not in ("", "?")]
        count = round(0.2 * len(observed))
        for index in rng.sample(observed, count):
            rows[index][column] = ""
        print(f"{column}: скрыто {count} из {len(observed)} значений.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
