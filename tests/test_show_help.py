from evargs import EvArgs, EvArgsException, ValidateException, HelpFormatter
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestShowHelp:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_help(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': int, 'help': 'This parameter set the default value. Default value is 5.', 'default': 5},
            'b': {'cast': int, 'help': 'This parameter is required. Max int value is 5.', 'required': True, 'validation': ('range', None, 5)},
            'c': {'cast': str, 'help': 'This parameter accepts a list of strings. Length is 1 - 5.', 'list': True, 'validation': ('sizes', 1, 5)},
            'd': {'cast': int, 'help': 'This parameter can accept multiple parameters.', 'multiple': True, 'validation': lambda v: v * 2},
            'e': {'cast': int, 'help': 'This parameter allows only the value of choices [1, 2, 3, 4]. Default value is 3.\nThis is e parameter sample message.\nSample message.', 'default': 3, 'choices': [1, 2, 3, 4]},
            'f': {'cast': str, 'help': 'This parameter is validated by alphabet format.', 'required': True, 'validation': 'alphabet'},
        })

        desc = evargs.make_help()

        assert re.search(r'This parameter', desc)

    def test_example(self):
        evargs = EvArgs()

        evargs.initialize({
            'star_mass': {'cast': float, 'help': ('Mass of the star in solar masses.', 'star_mass=1.5'), 'default': 1.0},
            'planet_count': {'cast': int, 'help': 'Number of planets orbiting the star.', 'required': True, 'validation': ['range', 0, 10]},
            'galaxy_type': {'cast': str, 'help': ('Type of galaxy.', 'spiral, elliptical'), 'choices': ['spiral', 'elliptical', 'irregular']},
            'distance': {'cast': float, 'help': 'Distance from Earth in light-years.', 'validation': lambda v: v > 0},
            'constellation': {'cast': str, 'help': ['Name of the constellation.', 'Centauri'], 'required': True, 'validation': 'alphabet'},
            'redshift': {'cast': float, 'help': 'Redshift value, indicating the expansion of the universe.', 'default': 0.0}
        })

        desc = evargs.make_help(append_example=True)

        assert re.search(r'Mass of the star', desc)

    def test_params(self):
        evargs = EvArgs()

        evargs.initialize({
            'ethane': {'cast': int, 'help': 'This parameter set the default value. Default value is 5.', 'default': 5},
            'methanol': {'cast': int, 'help': 'This parameter is required. Max int value is 5.', 'required': True, 'validation': ('range', None, 5)},
            'butane': {'cast': str, 'help': 'This parameter accepts a list of strings. Length is 1 - 5.', 'list': True, 'validation': ('sizes', 1, 5)},
            'propane': {'cast': int, 'help': 'This parameter can accept multiple parameters.', 'multiple': True, 'validation': lambda v: v * 2},
        })

        desc = evargs.make_help(params=['methanol'])

        assert re.search(r'methanol', desc)
        assert not re.search(r'butane', desc)

    def test_skip_headers(self):
        evargs = EvArgs()

        evargs.initialize({
            'ethane': {'cast': int, 'help': 'This parameter set the default value. Default value is 5.', 'default': 5},
            'methanol': {'cast': int, 'help': 'This parameter is required. Max int value is 5.', 'required': True, 'validation': ['range', None, 5]},
            'butane': {'cast': str, 'help': 'This parameter accepts a list of strings. Length is 1 - 5.', 'list': True, 'validation': ['sizes', 1, 5]},
            'propane': {'cast': int, 'help': 'This parameter can accept multiple parameters.', 'multiple': True, 'validation': lambda v: v * 2},
        })

        desc = evargs.make_help(skip_headers=True)

        assert not re.search(r'Description', desc)

    def test_set_column(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'cast': int, 'help': 'This parameter sets the maximum value. Default value is 10.', 'default': 10},
            'ruby': {'cast': int, 'help': 'This parameter is required. Max int value is 7.', 'required': True, 'validation': ['range', 1, 7]},
            'emerald': {'cast': str, 'help': 'This parameter accepts a list of strings.', 'list': True}
        })

        help_formatter = evargs.get_help_formatter()

        help_formatter.set_column('name', 'NAME')

        desc = evargs.make_help()

        assert re.search(r'NAME', desc)

    def test_set_columns(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'cast': int, 'help': 'This parameter sets the maximum value. Default value is 10.', 'default': 10},
            'ruby': {'cast': int, 'help': 'This parameter is required. Max int value is 7.', 'required': True, 'validation': ['range', 1, 7]},
            'emerald': {'cast': str, 'help': 'This parameter accepts a list of strings.', 'list': True}
        })

        help_formatter = evargs.get_help_formatter()

        help_formatter.set_columns({
            'name': 'Name',
            'required': '*',
            'cast': 'Cast-type',
            'help': 'Desc'
        })

        desc = evargs.make_help()

        assert re.search(r'Desc', desc)

    def test_set_example_columns(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'cast': int, 'help': ('This parameter sets the maximum value. Default value is 10.', 20), 'default': 10},
            'ruby': {'cast': int, 'help': ('This parameter is required. Max int value is 7.', 5), 'required': True, 'validation': ['range', 1, 7]},
            'emerald': {'cast': str, 'help': ('This parameter accepts a list of strings.', '1, 3, 4'), 'list': True}
        })

        help_formatter = evargs.get_help_formatter()

        help_formatter.set_columns({
            'name': 'Name',
            'required': '*',
            'example': 'e.g.',
            'help': 'Desc'
        })

        desc = evargs.make_help()

        assert re.search(r'e.g.', desc)
        assert re.search(r'1, 3, 4', desc)

    def test_set_column_max_size(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'cast': int, 'help': ('This parameter sets the maximum value. Default value is 10.', 20), 'default': 10},
            'ruby': {'cast': int, 'help': ('This parameter is required. Max int value is 7.', 5), 'required': True, 'validation': ['range', 1, 7]},
            'emerald': {'cast': str, 'help': ('This parameter accepts a list of strings.', '1, 3, 4'), 'list': True}
        })

        evargs.get_help_formatter().set_column_max_size(30)

        desc = evargs.make_help()

        assert re.search(r'\|\s+is 10.', desc)

    def test_customize_class(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'cast': bool, 'help': 'This parameter sets bool value.', 'default': True},
            'ruby': {'cast': bool, 'help': 'This parameter is required.', 'required': True},
            'emerald': {'cast': str, 'help': 'This parameter accepts a list of strings.', 'list': True}
        })

        help_formatter = MyHelpFormatter()

        evargs.set_help_formatter(help_formatter)

        desc = evargs.make_help()

        assert re.search(r'\sY\s', desc)


class MyHelpFormatter(HelpFormatter):
    def _get_col_required(self, v: any, key: any, columns: dict):
        return 'Y' if v else 'N'
