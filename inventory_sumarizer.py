import csv
import sys
import logging
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def parse_csv(file_path: Optional[Path] = None) -> None:
    """
    Parses a CSV file and logs each row.

    Args:
        file_path (Optional[Path]): Path to the CSV file. Defaults to './example_file/example.csv'.

    Raises:
        SystemExit: If there is an error reading the CSV file.
    """
    file_path = file_path or Path('./example_file/example.csv')

    if not file_path.is_file():
        logging.error(f"File not found: {file_path}")
        sys.exit(1)

    try:
        with file_path.open(newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                logging.info(f"Row: {row}")
    except csv.Error as e:
        logging.critical(f"Error reading file {file_path}, line {reader.line_num}: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    parse_csv()
