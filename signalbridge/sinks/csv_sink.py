import csv
from pathlib import Path

def write_rows(path: str | Path, rows: list[dict]) -> Path:
    rows = list(rows)
    output_path = Path(path)

    if not rows:
        return output_path

    fieldnames = list(dict.fromkeys(key for row in rows for key in row.keys()))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_path
