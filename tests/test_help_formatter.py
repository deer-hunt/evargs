from evargs.help_formatter import HelpFormatter, BaseHelpFormatter
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestHelpFormatter:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_validate_alphabet(self):
        help_fomatter = HelpFormatter()

        desc = help_fomatter.make({
            'planet_name': {'type': str, 'help': 'Name of the planet.', 'require': True},
            'orbital_period': {'type': float, 'help': 'Time taken to complete one orbit around the Sun in Earth days.', 'validation': 'unsigned'},
            'gravity': {'type': float, 'help': 'Surface gravity of the planet in m/s2.', 'validation': lambda v: v > 0, 'default': 1.0},
            'color': {'type': str, 'help': 'Dominant color of the planet.'},
            'has_life': {'type': bool, 'help': 'Indicates if there is life on the planet.'}
        })

        assert re.search(r'Dominant color of the planet', desc)

    def test_electron_microscope_help_formatter(self):
        help_fomatter = ElectronMicroscopeOperation()

        text = help_fomatter.make({
            'operation_mode': {'operation': 'Set Operation Mode', 'description': 'Sets the operation mode of the electron microscope (e.g., TEM, SEM).', 'default': 'SEM', 'parameters': 'operation_mode=SEM'},
            'magnification_level': {'operation': 'Set Magnification Level', 'description': 'Sets the magnification level of the electron microscope.', 'default': '1000x', 'parameters': 'magnification_level=1000x'},
            'beam_voltage': {'operation': 'Adjust Beam Voltage', 'description': 'Adjusts the voltage of the electron beam.', 'default': '20kV', 'parameters': 'beam_voltage=20kV'},
            'vacuum_pressure': {'operation': 'Set Vacuum Pressure', 'description': 'Sets the vacuum pressure inside the microscope chamber.', 'default': '1e-5 Pa', 'parameters': 'vacuum_pressure="1e-5 Pa"'}
        })

        assert re.search(r'magnification_level', text)

    def test_chemistry_list(self):
        csv_help = ChemistryListHelp()

        text = csv_help.make([
            {'name': 'Aspirin', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Oxygen (O)'], 'molecular': 'C9H8O4', 'melting': '135°C', 'uses': 'Pain reliever'},
            {'name': 'Glucose', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Oxygen (O)'], 'molecular': 'C6H12O6', 'melting': '146°C', 'uses': 'Energy source'},
            {'name': 'Acetaminophen', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Nitrogen (N)', 'Oxygen (O)'], 'molecular': 'C8H9NO', 'melting': '169-172°C', 'uses': 'Pain reliever'},
            {'name': 'Niacin', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Nitrogen (N)'], 'molecular': 'C6H5NO2', 'melting': '234-236°C', 'uses': 'Nutrient'},
            {'name': 'Salicylic Acid', 'elements': ['Carbon (C)', 'Hydrogen (H)', 'Oxygen (O)'], 'molecular': 'C7H6O3', 'melting': '158-160°C', 'uses': 'Preservative'}
        ])

        assert re.search(r'C7H6O3', text)


class ElectronMicroscopeOperation(BaseHelpFormatter):
    def __init__(self):
        super().__init__()

        self.columns = {
            'operation': 'Operation',
            'description': 'Description',
            'default': 'Default',
            'parameters': 'Parameters'
        }

    def _get_col_default(self, v: any, *args):
        return f'"{v}"'


class ChemistryListHelp(BaseHelpFormatter):
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
