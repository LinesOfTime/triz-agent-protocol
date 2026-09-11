from .normalizer import normalize_date
from .writer import atomic_write


def import_rows(rows):
    normalized = [{**row, "date": normalize_date(row["date"])} for row in rows]
    atomic_write(normalized)
