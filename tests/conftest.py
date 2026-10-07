from pathlib import Path

import pytest

from nhs_stats.paths import DataPaths

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_csv() -> Path:
    return FIXTURES / "ae_monthly_2026-03.csv"


@pytest.fixture
def paths(tmp_path: Path) -> DataPaths:
    return DataPaths(tmp_path / "data")
