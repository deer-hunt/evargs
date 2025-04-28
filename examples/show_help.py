from evargs import EvArgs, EvArgsException, ValidateException, HelpFormatter
import json

'''
python3 show_help.py
'''


def main():
    evargs = EvArgs()

    evargs.initialize({
        'planet_name': {'cast': str, 'help': ('Name of the planet.', 'Jupiter'), 'required': True},
        'distance_from_sun': {'cast': float, 'help': 'Distance from the Sun in kilometers.', 'validation': 'unsigned'},
        'diameter': {'cast': float, 'help': ('Diameter of the planet in kilometers.', 6779), 'validation': lambda v: v > 0},
        'has_water': {'cast': bool, 'help': ('Indicates if the planet has water.', 1), 'default': False},
        'surface_color': {'cast': str, 'help': ('Main color of the surface.', 'Black')}
    })

    evargs.set_help_formatter(MyHelpFormatter())

    evargs.get_help_formatter().set_columns({
        'name': 'Name',
        'required': '*',
        'example': 'e.g.',
        'validation': 'Validation',
        'help': 'Description'
    })

    print('[show_help.py help]\n')
    print(evargs.make_help(append_example=True))


class MyHelpFormatter(HelpFormatter):
    def _get_col_required(self, v, key, columns):
        return 'Y' if v else 'N'


if __name__ == "__main__":
    main()
