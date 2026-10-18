import pytest

from querypilot.tools.validator import validate_sql


@pytest.mark.parametrize("q", [
    "SELECT * FROM Customer",
    "WITH t AS (SELECT 1) SELECT * FROM t",
    "SELECT a FROM x UNION SELECT b FROM y",
])
def test_allows_select(q):
    assert validate_sql(q).ok


@pytest.mark.parametrize("q", [
    "DROP TABLE Customer",
    "DELETE FROM Customer",
    "UPDATE Customer SET Email='x'",
    "INSERT INTO Customer VALUES (1)",
    "SELECT 1; DROP TABLE Customer",
    "PRAGMA writable_schema=1",
    "ATTACH DATABASE 'x.db' AS x",
])
def test_blocks_harmful(q):
    assert not validate_sql(q).ok
