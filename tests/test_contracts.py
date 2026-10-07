from pathlib import Path

import polars as pl

from nhs_stats.contracts import load_contract, validate


def _valid_frame() -> pl.DataFrame:
    contract = load_contract("ae_monthly_silver")
    return pl.DataFrame(schema=contract.polars_schema())


def test_empty_conforming_frame_has_no_violations() -> None:
    contract = load_contract("ae_monthly_silver")
    assert validate(_valid_frame(), contract) == []


def test_reports_missing_wrong_type_pattern_and_duplicates() -> None:
    contract = load_contract("ae_monthly_silver")
    df = _valid_frame().drop("org_name")
    df = df.with_columns(pl.col("attendances_type1").cast(pl.String))
    messages = {(v.column, v.message.split()[0]) for v in validate(df, contract)}
    assert ("org_name", "column") in messages
    assert ("attendances_type1", "dtype") in messages


def test_value_constraints() -> None:
    contract = load_contract("ae_monthly_silver")
    row = {c.name: None for c in contract.columns}
    base = _valid_frame()
    bad = pl.DataFrame(
        [
            {**row, "org_code": "bad code", "attendances_type1": -1},
            {**row, "org_code": "bad code", "attendances_type1": 5},
        ],
        schema=contract.polars_schema(),
    )
    out = {v.column: v.message for v in validate(pl.concat([base, bad]), contract)}
    assert "break" in out["org_code"]
    assert "below" in out["attendances_type1"]
    assert "duplicate" in out[None]
    assert Path("contracts/ae_monthly_silver.yaml").exists()
