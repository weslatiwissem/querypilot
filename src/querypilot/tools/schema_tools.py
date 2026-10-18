"""list_tables, describe_table, sample_rows (Phase 1)."""
import sqlite3


def _ro(db_path: str):
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


def list_tables(db_path: str) -> list[str]:
    with _ro(db_path) as c:
        return [r[0] for r in c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]


def describe_table(db_path: str, name: str) -> dict:
    if name not in list_tables(db_path):
        raise ValueError(f"Unknown table: {name}")
    with _ro(db_path) as c:
        cols = [{"name": r[1], "type": r[2], "pk": bool(r[5])}
                for r in c.execute(f'PRAGMA table_info("{name}")')]
        fks = [{"from": r[3], "table": r[2], "to": r[4]}
               for r in c.execute(f'PRAGMA foreign_key_list("{name}")')]
    return {"table": name, "columns": cols, "foreign_keys": fks}


def sample_rows(db_path: str, table: str, n: int = 3) -> list[tuple]:
    if table not in list_tables(db_path):
        raise ValueError(f"Unknown table: {table}")
    with _ro(db_path) as c:
        return c.execute(f'SELECT * FROM "{table}" LIMIT {int(n)}').fetchall()
