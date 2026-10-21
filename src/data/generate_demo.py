"""Создание синтетических сессий для проверки хранения данных Cart Scope."""

import argparse
import csv
import random
from pathlib import Path


DEFAULT_OUTPUT = Path(__file__).resolve().parents[2] / "data/raw/demo_sessions.csv"
FIELDS = ("session_id", "duration_seconds", "products_viewed", "purchased")


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("Число строк должно быть больше нуля.")
    return number


def generate_demo(output: Path, rows: int = 100, seed: int = 42) -> None:
    """Записать CSV; одинаковые параметры дают одинаковые байты файла."""
    if rows < 1:
        raise ValueError("Число строк должно быть больше нуля.")
    rng = random.Random(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Режим x защищает исходные данные от случайной перезаписи.
    with output.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        for index in range(1, rows + 1):
            writer.writerow(
                {
                    "session_id": f"demo_{index:04d}",
                    "duration_seconds": rng.randint(10, 1800),
                    "products_viewed": rng.randint(1, 20),
                    "purchased": int(rng.random() < 0.2),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Путь к новому CSV.")
    parser.add_argument("--rows", type=positive_int, default=100, help="Количество сессий (100).")
    parser.add_argument("--seed", type=int, default=42, help="Seed генератора (42).")
    args = parser.parse_args()
    try:
        generate_demo(args.output, args.rows, args.seed)
    except FileExistsError:
        parser.error("Файл уже существует. Укажите новый путь через --output.")
    print(f"Создано {args.rows} синтетических сессий: {args.output}")


if __name__ == "__main__":
    main()
