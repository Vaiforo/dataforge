"""Добавить 10% копий сессий с искусственными пропусками в отдельный набор."""

import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/raw/online_shoppers_intention.csv"
OUTPUT = ROOT / "data/processed/online_shoppers_with_missing.csv"
SEED = 42


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        rows = list(reader)
    if not fields or "Revenue" not in fields or not rows:
        raise ValueError("Ожидается непустой CSV с целевым столбцом Revenue.")
    features = [field for field in fields if field != "Revenue"]
    if len(features) < 2:
        raise ValueError("Нужно не менее двух признаков.")
    if OUTPUT.exists():
        raise FileExistsError("Выходной файл уже существует; перезапись запрещена.")

    rng = random.Random(SEED)
    added_count = round(len(rows) * 0.1)
    augmented = list(rows)
    for source_index in rng.sample(range(len(rows)), added_count):
        new_row = rows[source_index].copy()
        for field in rng.sample(features, 2):
            new_row[field] = ""
        augmented.append(new_row)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(augmented)
    print(f"Исходных строк: {len(rows)}, добавлено: {added_count}, всего: {len(augmented)}.")


if __name__ == "__main__":
    main()
