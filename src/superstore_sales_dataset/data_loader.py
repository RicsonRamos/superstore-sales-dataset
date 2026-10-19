"""Dataset download and storage module.

Downloads the Superstore dataset from Kaggle and stores the CSV
file in the project's standardized raw data directory.
"""

import shutil
from pathlib import Path

import kagglehub

from superstore_sales_dataset.config import RAW_DATA_DIR


class DatasetNotFoundError(FileNotFoundError):
    """Raised when no CSV file is found in the downloaded dataset."""

    def __init__(self, dataset_dir: Path) -> None:
        super().__init__(f"No CSV file found in the downloaded dataset: {dataset_dir}")


def load_data() -> Path:
    """Download the dataset if needed and return its local CSV path."""

    destination = RAW_DATA_DIR / "superstore_sales_dataset.csv"

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if destination.is_file():
        return destination

    dataset_dir = Path(kagglehub.dataset_download("vivek468/superstore-dataset-final"))

    csv_files = sorted(dataset_dir.rglob("*.csv"))

    if not csv_files:
        raise DatasetNotFoundError(dataset_dir)

    # Prefer the expected dataset filename when available.
    source = next(
        (
            path
            for path in csv_files
            if path.name.lower() == "superstore_sales_dataset.csv"
        ),
        csv_files[0],
    )

    shutil.copy2(source, destination)

    return destination


if __name__ == "__main__":
    path = load_data()
    print(f"Dataset available at: {path}")
