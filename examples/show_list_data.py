from evargs.help_formatter import BaseHelpFormatter

'''
python3 show_list_data.py
'''


def main():
    csv_help = ListDataHelpFormatter()

    text = csv_help.make([
        {'name': 'Aspirin', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Oxygen (O)'], 'molecular': 'C9H8O4', 'melting': '135°C', 'uses': 'Pain reliever'},
        {'name': 'Glucose', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Oxygen (O)'], 'molecular': 'C6H12O6', 'melting': '146°C', 'uses': 'Energy source'},
        {'name': 'Acetaminophen', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Nitrogen (N)', 'Oxygen (O)'], 'molecular': 'C8H9NO', 'melting': '169-172°C', 'uses': 'Pain reliever'},
        {'name': 'Niacin', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Nitrogen (N)'], 'molecular': 'C6H5NO2', 'melting': '234-236°C', 'uses': 'Nutrient'},
        {'name': 'Salicylic Acid', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Oxygen (O)'], 'molecular': 'C7H6O3', 'melting': '158-160°C', 'uses': 'Preservative'}
    ])

    print('[List data]\n')

    print(text)


class ListDataHelpFormatter(BaseHelpFormatter):
    def __init__(self):
        super().__init__()

        self.columns = {
            'name': 'Compound Name',
            'elements': 'Elements',
            'molecular': 'Molecular Formula',
            'melting': 'Melting Point',
            'uses': 'Uses'
        }

    def _get_col_elements(self, v: any, *args):
        return ', '.join(v)


if __name__ == "__main__":
    main()
