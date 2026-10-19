"""Smoke tests ensuring basic project structure and package imports succeed."""

from superstore_sales_dataset.config import (
    DATA_DIR,
    MODELS_DIR,
    NOTEBOOKS_DIR,
    PROJ_ROOT,
    REPORTS_DIR,
)


def test_project_root_exists() -> None:
    """Verify project root path exists."""
    assert PROJ_ROOT.exists()


def test_standard_directories_exist() -> None:
    """Verify standard data science directories exist."""
    assert DATA_DIR.exists()
    assert MODELS_DIR.exists()
    assert NOTEBOOKS_DIR.exists()
    assert REPORTS_DIR.exists()
