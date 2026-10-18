"""run_query: read-only connection, timeout, row cap."""
import sqlite3
import time
from dataclasses import dataclass

from .validator import validate_sql


@dataclass
class QueryResult:
    columns: list[str]
    rows: list[tuple]
    truncated: bool


class QueryError(Exception):
    pass


def run_query(db_path: str, query: str, limit: int = 100, timeout: float = 10.0) -> QueryResult:
    v = validate_sql(query)
    if not v.ok:
        raise QueryError(v.error)
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    deadline = time.monotonic() + timeout
    conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 10_000)
    try:
        cur = conn.execute(query)
        cols = [d[0] for d in cur.description or []]
        rows = cur.fetchmany(limit + 1)
        return QueryResult(cols, rows[:limit], len(rows) > limit)
    except sqlite3.Error as e:
        raise QueryError(str(e)) from e
    finally:
        conn.close()
