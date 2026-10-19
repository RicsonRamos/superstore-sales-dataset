"""Dataset download and storage module.

Downloads the Superstore dataset from Kaggle and stores the CSV
file in the project's standardized raw data directory.
"""

import shutil
from pathlib import Path

import kagglehub

# Import the raw data directory defined in config.py
from config import RAW_DATA_DIR


class DatasetNotFoundError(FileNotFoundError):
    """Raised when the downloaded Kaggle dataset does not contain a CSV file."""

    def __init__(self, dataset_dir: Path) -> None:
        super().__init__(f"No CSV file found in the downloaded dataset: {dataset_dir}")


def load_data() -> None:
    """Download the dataset and store it in the raw data directory."""

    # Define the destination path using the project's configuration
    destination = RAW_DATA_DIR / "superstore_sales_dataset.csv"

    # Check whether the dataset already exists to avoid unnecessary downloads
    if destination.exists():
        print(f"Dataset already exists at: {destination}")
        return

    # Create the raw data directory if it does not already exist
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Download the dataset from KaggleHub
    # KaggleHub returns the path to the downloaded dataset in its cache
    dataset_dir = Path(kagglehub.dataset_download("vivek468/superstore-dataset-final"))

    # Search for CSV files in the downloaded directory and its subdirectories
    csv_files = list(dataset_dir.rglob("*.csv"))

    # Raise an error if no CSV files are found in the downloaded dataset
    if not csv_files:
        raise DatasetNotFoundError(dataset_dir)

    # Select the first CSV file found in the dataset
    source = csv_files[0]

    # Copy the CSV file to the project's raw data directory
    # The destination filename is standardized for the project
    shutil.copy2(source, destination)

    # Display the source and destination paths for confirmation
    print(f"Dataset copied from: {source}")
    print(f"Dataset saved to: {destination}")


if __name__ == "__main__":
    load_data()
