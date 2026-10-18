"""validate_sql: only a single read-only SELECT is allowed."""
from dataclasses import dataclass

import sqlglot
from sqlglot import exp

_FORBIDDEN_NAMES = [
    "Insert", "Update", "Delete", "Drop", "Create", "Alter", "Merge",
    "Command", "Pragma", "Attach", "Detach", "TruncateTable", "Copy", "Set",
]
FORBIDDEN = tuple(getattr(exp, n) for n in _FORBIDDEN_NAMES if hasattr(exp, n))
ALLOWED_ROOTS = (exp.Select, exp.Union, exp.Intersect, exp.Except)


@dataclass
class Validation:
    ok: bool
    error: str | None = None


def validate_sql(query: str, dialect: str = "sqlite") -> Validation:
    try:
        statements = [s for s in sqlglot.parse(query, read=dialect) if s is not None]
    except sqlglot.errors.ParseError as e:
        return Validation(False, f"Syntax error: {e}")
    if len(statements) != 1:
        return Validation(False, "Exactly one statement is allowed.")
    tree = statements[0]
    if not isinstance(tree, ALLOWED_ROOTS):
        return Validation(False, "Only SELECT queries are allowed.")
    for node in tree.walk():
        if isinstance(node, FORBIDDEN):
            return Validation(False, f"Forbidden operation: {type(node).__name__}")
    return Validation(True)
