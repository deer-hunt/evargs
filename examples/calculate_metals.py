from evargs import ExpEvArgs, EvArgsException, ValidateException
import sys

'''
python3 calculate_metals.py "silver=1;gold=1;platinum=1;"
'''


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 calculate_metals.py "silver=1;gold=1;platinum=1;"')
        sys.exit(1)

    evargs = ExpEvArgs()

    evargs.initialize({
        'silver': {'cast': int, 'default': 1, 'validation': ['range', 1, 100]},
        'gold': {'cast': int, 'default': 2, 'validation': ['range', 0, 100]},
        'platinum': {'cast': int, 'default': 0, 'validation': ['range', 0, 100]},
        'msg': {'cast': str, 'default': 'Total Metals'}
    })

    argument = sys.argv[1]

    try:
        evargs.parse(argument)
    except ValidateException as e:
        print(str(e))
        sys.exit(1)

    print(evargs.get('msg') + ':\n')

    defines = {
        'silver': 10.49,
        'gold': 19.32,
        'platinum': 21.45,
    }

    silver_g = calc_g(defines, evargs, 'silver')
    gold_g = calc_g(defines, evargs, 'gold')
    platinum_g = calc_g(defines, evargs, 'platinum')

    print('Silver: {}cm³ = {}g'.format(evargs.get('silver'), silver_g))
    print('Gold: {}cm³ = {}g'.format(evargs.get('gold'), gold_g))
    print('Platinum: {}cm³ = {}g'.format(evargs.get('platinum'), platinum_g))

    total_g = round(silver_g + gold_g + platinum_g, 2)

    print('\nTotal: {}g'.format(total_g))


def calc_g(defines, evargs, metal):
    n = evargs.get(metal)

    return defines[metal] * n


if __name__ == "__main__":
    main()
