from evargs import EvArgs, EvArgsException, EvValidateException, HelpFormatter
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestGeneral:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_help(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'help': 'This parameter set the default value. Default value is 5.', 'default': 5},
            'b': {'type': int, 'help': 'This parameter is required. Max int value is 5.', 'require': True, 'validation': ['range', None, 5]},
            'c': {'type': str, 'help': 'This parameter accepts a list of strings. Length is 1 - 5.', 'list': True, 'validation': ['between', 1, 5]},
            'd': {'type': int, 'help': 'This parameter can accept multiple parameters.', 'multiple': True, 'validation': lambda v: v * 2},
            'e': {'type': int, 'help': 'This parameter allows only the value of choices [1, 2, 3, 4]. Default value is 3.\nThis is e parameter sample message.\nSample message.', 'default': 3, 'choices': [1, 2, 3, 4]},
            'f': {'type': str, 'help': 'This parameter is validated by alphabet format.', 'require': True, 'validation': 'alphabet'},
        })

        desc = evargs.make_help()

        assert re.search(r'This parameter', desc)

    def test_example(self):
        evargs = EvArgs()

        evargs.initialize({
            'star_mass': {'type': float, 'help': ('Mass of the star in solar masses.', 'star_mass=1.5'), 'default': 1.0},
            'planet_count': {'type': int, 'help': 'Number of planets orbiting the star.', 'require': True, 'validation': ['range', 0, 10]},
            'galaxy_type': {'type': str, 'help': ('Type of galaxy.', 'spiral, elliptical'), 'choices': ['spiral', 'elliptical', 'irregular']},
            'distance': {'type': float, 'help': 'Distance from Earth in light-years.', 'validation': lambda v: v > 0},
            'constellation': {'type': str, 'help': ['Name of the constellation.', 'Centauri'], 'require': True, 'validation': 'alphabet'},
            'redshift': {'type': float, 'help': 'Redshift value, indicating the expansion of the universe.', 'default': 0.0}
        })

        desc = evargs.make_help(append_example=True)

        assert re.search(r'Mass of the star', desc)

    def test_params(self):
        evargs = EvArgs()

        evargs.initialize({
            'ethane': {'type': int, 'help': 'This parameter set the default value. Default value is 5.', 'default': 5},
            'methanol': {'type': int, 'help': 'This parameter is required. Max int value is 5.', 'require': True, 'validation': ['range', None, 5]},
            'butane': {'type': str, 'help': 'This parameter accepts a list of strings. Length is 1 - 5.', 'list': True, 'validation': ['between', 1, 5]},
            'propane': {'type': int, 'help': 'This parameter can accept multiple parameters.', 'multiple': True, 'validation': lambda v: v * 2},
        })

        desc = evargs.make_help(params=['methanol'])

        assert re.search(r'methanol', desc)
        assert not re.search(r'butane', desc)

    def test_skip_headers(self):
        evargs = EvArgs()

        evargs.initialize({
            'ethane': {'type': int, 'help': 'This parameter set the default value. Default value is 5.', 'default': 5},
            'methanol': {'type': int, 'help': 'This parameter is required. Max int value is 5.', 'require': True, 'validation': ['range', None, 5]},
            'butane': {'type': str, 'help': 'This parameter accepts a list of strings. Length is 1 - 5.', 'list': True, 'validation': ['between', 1, 5]},
            'propane': {'type': int, 'help': 'This parameter can accept multiple parameters.', 'multiple': True, 'validation': lambda v: v * 2},
        })

        desc = evargs.make_help(skip_headers=True)

        assert not re.search(r'Description', desc)

    def test_set_column(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'type': int, 'help': 'This parameter sets the maximum value. Default value is 10.', 'default': 10},
            'ruby': {'type': int, 'help': 'This parameter is required. Max int value is 7.', 'require': True, 'validation': ['range', 1, 7]},
            'emerald': {'type': str, 'help': 'This parameter accepts a list of strings.', 'list': True}
        })

        help_formatter = evargs.get_help_formatter()

        help_formatter.set_column('name', 'NAME')

        desc = evargs.make_help()

        assert re.search(r'NAME', desc)

    def test_set_columns(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'type': int, 'help': 'This parameter sets the maximum value. Default value is 10.', 'default': 10},
            'ruby': {'type': int, 'help': 'This parameter is required. Max int value is 7.', 'require': True, 'validation': ['range', 1, 7]},
            'emerald': {'type': str, 'help': 'This parameter accepts a list of strings.', 'list': True}
        })

        help_formatter = evargs.get_help_formatter()

        help_formatter.set_columns({
            'name': 'Name',
            'require': '*',
            'type': 'Type',
            'help': 'Desc'
        })

        desc = evargs.make_help()

        assert re.search(r'Desc', desc)

    def test_set_example_columns(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'type': int, 'help': ('This parameter sets the maximum value. Default value is 10.', 20), 'default': 10},
            'ruby': {'type': int, 'help': ('This parameter is required. Max int value is 7.', 5), 'require': True, 'validation': ['range', 1, 7]},
            'emerald': {'type': str, 'help': ('This parameter accepts a list of strings.', '1, 3, 4'), 'list': True}
        })

        help_formatter = evargs.get_help_formatter()

        help_formatter.set_columns({
            'name': 'Name',
            'require': '*',
            'example': 'e.g.',
            'help': 'Desc'
        })

        desc = evargs.make_help()

        assert re.search(r'e.g.', desc)
        assert re.search(r'1, 3, 4', desc)

    def test_set_column_max_size(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'type': int, 'help': ('This parameter sets the maximum value. Default value is 10.', 20), 'default': 10},
            'ruby': {'type': int, 'help': ('This parameter is required. Max int value is 7.', 5), 'require': True, 'validation': ['range', 1, 7]},
            'emerald': {'type': str, 'help': ('This parameter accepts a list of strings.', '1, 3, 4'), 'list': True}
        })

        evargs.get_help_formatter().set_column_max_size(30)

        desc = evargs.make_help()

        assert re.search(r'\|\s+is 10.', desc)

    def test_customize_class(self):
        evargs = EvArgs()

        evargs.initialize({
            'diamond': {'type': bool, 'help': 'This parameter sets bool value.', 'default': True},
            'ruby': {'type': bool, 'help': 'This parameter is required.', 'require': True},
            'emerald': {'type': str, 'help': 'This parameter accepts a list of strings.', 'list': True}
        })

        help_formatter = MyHelpFormatter()

        evargs.set_help_formatter(help_formatter)

        desc = evargs.make_help()

        assert re.search(r'\sY\s', desc)


class MyHelpFormatter(HelpFormatter):
    def _get_col_require(self, v: any, key: any, columns: dict):
        return 'Y' if v else 'N'
