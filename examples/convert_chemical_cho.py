import argparse
import re
from evargs import EvArgs

'''
python3 convert_chemical_cho.py --water=' H₂O' --carbon_dioxide=' CO₂ ' --methane=' CH₄ '
'''


class CHOCompound:
    def __init__(self):
        self.name = ''

        self.item_c = 0
        self.item_h = 0
        self.item_o = 0


def main():
    parser = argparse.ArgumentParser(description='Chemical formula parameters.')

    parser.add_argument('--water', type=str, required=True, help='Chemical formula for water')
    parser.add_argument('--carbon_dioxide', type=str, required=True, help='Chemical formula for carbon dioxide')
    parser.add_argument('--methane', type=str, required=True, help='Chemical formula for methane')

    args = parser.parse_args()

    params = vars(args)

    evargs = EvArgs()

    def convert(v):
        compound = CHOCompound()
        compound.name = v

        matches = re.findall(r'([CHO])(\d*|[₁₂₃₄₅₆₇₈₉]*)', v)

        for element, count in matches:
            if not count:
                count = 1
            else:
                count = int(count) if count else 1

            if element == 'C':
                compound.item_c += count
            elif element == 'H':
                compound.item_h += count
            elif element == 'O':
                compound.item_o += count

        return compound

    def normalize(v):
        replacements = {
            '₁': '1',
            '₂': '2',
            '₃': '3',
            '₄': '4',
            '₅': '5',
            '₆': '6',
            '₇': '7',
            '₈': '8',
            '₉': '9',
            '₀': '0'
        }

        for sub, normal in replacements.items():
            v = v.replace(sub, normal)

        return v

    evargs.initialize({
        'water': {'trim': True, 'post_cast': normalize, 'choices': ['H2O', 'H+', 'OH⁻', 'O2'], 'post_apply': convert},
        'carbon_dioxide': {'trim': True, 'post_cast': normalize, 'choices': ['CO2', 'CO', '¹³C', 'C', 'O2'], 'post_apply': convert},
        'methane': {'trim': True, 'post_cast': normalize, 'choices': ['CH4', 'CO', '	H2O', 'CO2', 'C'], 'post_apply': convert}
    })

    evargs.put_values(params)

    for name, compound in evargs.get_values().items():
        print(f'{compound.name} -> C:{compound.item_c},H:{compound.item_h},O:{compound.item_o}')


if __name__ == '__main__':
    main()
