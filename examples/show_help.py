from evargs import EvArgs, EvArgsException, EvValidateException, HelpFormatter
import json

'''
python3 show_help.py
'''


def main():
    evargs = EvArgs()

    evargs.initialize({
        'planet_name': {'type': str, 'help': ('Name of the planet.', 'Jupiter'), 'require': True},
        'distance_from_sun': {'type': float, 'help': 'Distance from the Sun in kilometers.', 'validation': 'unsigned'},
        'diameter': {'type': float, 'help': ('Diameter of the planet in kilometers.', 6779), 'validation': lambda v: v > 0},
        'has_water': {'type': bool, 'help': ('Indicates if the planet has water.', 1), 'default': False},
        'surface_color': {'type': str, 'help': ('Main color of the surface.', 'Black')}
    })

    evargs.set_help_formatter(MyHelpFormatter())

    evargs.get_help_formatter().set_columns({
        'name': 'Name',
        'require': '*',
        'example': 'e.g.',
        'validation': 'Validation',
        'help': 'Description'
    })

    print('[show_help.py help]\n')
    print(evargs.make_help(append_example=True))


class MyHelpFormatter(HelpFormatter):
    def _get_col_require(self, v, key, columns):
        return 'Y' if v else 'N'


if __name__ == "__main__":
    main()
