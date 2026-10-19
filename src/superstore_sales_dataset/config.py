"""Project configuration module.

Provides standardized filesystem paths using pathlib and automatically
loads environment variables from the project root .env file.
"""

from pathlib import Path

from dotenv import load_dotenv

# Root directory of the repository (two levels up from src/<package_name>/)
PROJ_ROOT = Path(__file__).resolve().parents[2]

# Standard Data Science directories
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "01_raw"
INTERIM_DATA_DIR = DATA_DIR / "02_interim"
PROCESSED_DATA_DIR = DATA_DIR / "03_processed"
EXTERNAL_DATA_DIR = DATA_DIR / "04_external"

MODELS_DIR = PROJ_ROOT / "models"
NOTEBOOKS_DIR = PROJ_ROOT / "notebooks"
REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Automatically load environment variables from .env if present
load_dotenv(PROJ_ROOT / ".env")


def info() -> None:
    """Print high-level project configuration and standard paths."""
    print("=" * 60)
    print("Project Configuration Summary")
    print("=" * 60)
    print(f"Project Root   : {PROJ_ROOT}")
    print(f"Raw Data       : {RAW_DATA_DIR}")
    print(f"Interim Data   : {INTERIM_DATA_DIR}")
    print(f"Processed Data : {PROCESSED_DATA_DIR}")
    print(f"External Data  : {EXTERNAL_DATA_DIR}")
    print(f"Models Dir     : {MODELS_DIR}")
    print(f"Notebooks Dir  : {NOTEBOOKS_DIR}")
    print(f"Reports Dir    : {REPORTS_DIR}")
    print(f"Figures Dir    : {FIGURES_DIR}")
    print("=" * 60)
