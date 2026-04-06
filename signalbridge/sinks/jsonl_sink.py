import json
from pathlib import Path


def write_rows(path: str | Path, rows: list[dict]) -> Path:
    """Write a list of dictionary rows to JSONL and return the destination path."""
    rows = list(rows)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        output_path.write_text("", encoding="utf-8")
        return output_path

    with output_path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row))
            file.write("\n")

    return output_path
