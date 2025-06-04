import csv
import sys
import logging
from collections import defaultdict
from pathlib import Path
from typing import Optional, Dict


INVENTORY_TITLE = 'INVENTORY SUMMARY'
LINE_WIDTH = 80

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def parse_csv(file_path: Optional[Path] = None) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Parse an inventory CSV file into a nested dictionary.

    Args:
        file_path (Optional[Path]): Path to the CSV file.

    Returns:
        dict: Nested structure {CATEGORY -> {PRODUCT -> {UNIT_TYPE -> QUANTITY}}}
    """
    file_path = file_path or Path('./example_file/example.csv')

    if not file_path.is_file():
        logging.critical(f"File not found: {file_path}")
        sys.exit(1)

    inventory = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    try:
        with file_path.open(newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            expected_fields = {'CATEGORY', 'PRODUCT', 'QUANTITY', 'UNIT_TYPE'}
            if set(reader.fieldnames or []) != expected_fields:
                raise ValueError(
                    f'Invalid CSV header. Expected fields: {", ".join(expected_fields)}'
                )

            for row in reader:
                try:
                    category = row['CATEGORY'].strip().title()
                    product = row['PRODUCT'].strip().title()
                    unit = row['UNIT_TYPE'].strip().lower()
                    quantity = float(row['QUANTITY'].replace(',', '.'))

                    inventory[category][product][unit] += quantity

                except (ValueError, KeyError) as e:
                    logging.warning(f"Skipping invalid row {row}: {e}")

    except (csv.Error, IOError) as e:
        logging.critical(f"Failed reading CSV file '{file_path}': {e}")
        sys.exit(1)

    return inventory


def print_inventory(inventory: Dict[str, Dict[str, Dict[str, float]]]) -> None:
    """
    Prints the inventory in a structured format.
    """
    separator = '=' * LINE_WIDTH
    print(separator)
    print(INVENTORY_TITLE.center(LINE_WIDTH))
    print(separator)

    for category, products in sorted(inventory.items()):
        print(f"\n{category.upper()}")
        print('-' * LINE_WIDTH)

        for product, units in sorted(products.items()):
            for unit, quantity in sorted(units.items()):
                unit_display = unit + ('s' if not unit.endswith('s') else '')
                print(f"{product.lower():<30} {quantity:>8.0f} {unit_display}")

    print('\n' + separator)


if __name__ == '__main__':
    csv_data = parse_csv()
    print_inventory(csv_data)
