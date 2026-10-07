"""Gold layer: dashboard-serving tables built with DuckDB SQL over silver parquet."""

from __future__ import annotations

from pathlib import Path

import duckdb

from nhs_stats.resources import sql_dir


def build_table(sql_file: str, silver_glob: str, output: Path) -> int:
    """Run sql/gold/<sql_file> against silver and write parquet; returns the row count."""
    query = (sql_dir() / "gold" / sql_file).read_text(encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect() as con:
        con.execute("SET TimeZone = 'UTC'")
        con.execute(
            f"CREATE TEMP VIEW silver AS SELECT * FROM read_parquet({_literal(silver_glob)})"
        )
        con.execute(f"COPY ({query}) TO {_literal(str(output))} (FORMAT PARQUET, COMPRESSION ZSTD)")
        row = con.execute(f"SELECT count(*) FROM read_parquet({_literal(str(output))})").fetchone()
    return int(row[0]) if row else 0


def _literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
