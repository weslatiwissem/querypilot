import sqlite3

import pytest

from querypilot.tools.executor import QueryError, run_query


@pytest.fixture
def db(tmp_path):
    p = tmp_path / "t.db"
    c = sqlite3.connect(p)
    c.execute("CREATE TABLE t (x INT)")
    c.executemany("INSERT INTO t VALUES (?)", [(i,) for i in range(50)])
    c.commit()
    c.close()
    return str(p)


def test_row_cap(db):
    r = run_query(db, "SELECT * FROM t", limit=10)
    assert len(r.rows) == 10 and r.truncated


def test_rejects_write(db):
    with pytest.raises(QueryError):
        run_query(db, "DELETE FROM t")
