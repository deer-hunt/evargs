import re
import textwrap
from typing import Union


class BaseHelpFormatter:
    def __init__(self):
        self.columns = {}

        self.column_max_size = 160

    def set_columns(self, columns: dict):
        self.columns = columns

    def set_column(self, name: str, value: any):
        self.columns[name] = value

    def set_column_max_size(self, v: int):
        self.column_max_size = v

    def make(self, rows: Union[list, dict], params: list = None, skip_headers: bool = False) -> str:
        if params is not None:
            rows = self._filter_rows(rows, params)

        headers = [label for name, label in self.columns.items()]

        output_rows = []

        if isinstance(rows, dict):
            iter_rows = rows.items()
        else:
            iter_rows = enumerate(rows)

        for key, row in iter_rows:
            output_rows.append(self._create_row(key, row))

        col_sizes = self._calc_column_sizes(headers, output_rows)

        output_text = ''

        if not skip_headers:
            output_text += self._make_head_text(col_sizes, headers)

        for output_row in output_rows:
            for row in self._normalize_row_values(output_row):
                output_text += self._make_row_text(col_sizes, row)

        return output_text

    def _filter_rows(self, rows: list, params: list = None):
        rows = {key: rows[key] for key in params if key in rows}

        return rows

    def _create_row(self, key: any, columns: dict):
        row = [self._get_column_value(key, columns, cur) for cur, v in self.columns.items()]

        return row

    def _make_head_text(self, col_sizes: list, headers: list):
        header_text = self._make_row_text(col_sizes, headers)

        header_text += '-' * len(header_text) + '\n'

        return header_text

    def _calc_column_sizes(self, headers: list, rows: list):
        col_sizes = []

        for column in zip(headers, *rows):
            max_size = 0

            for item in column:
                max_size = max(max_size, len(str(item)))

                max_size = max_size if self.column_max_size > max_size else self.column_max_size

            col_sizes.append(max_size)

        return col_sizes

    def _make_row_text(self, col_sizes: list, columns: list):
        values = []

        for i, v in enumerate(columns):
            values.append('{:<{}}'.format(v, col_sizes[i]))

        row_text = ' | '.join(values)
        row_text = f' {row_text} \n'

        return row_text

    def _normalize_row_values(self, row: list):
        appends = []

        for i, v in enumerate(row):
            if isinstance(v, str):
                v = textwrap.fill(v, width=self.column_max_size, replace_whitespace=False)

                (v, ts) = self._split_value(v)

                for j, t in enumerate(ts):
                    if j >= len(appends):
                        appends.append([''] * len(row))

                    appends[j][i] = t

            row[i] = v

        return [row] + appends

    def _split_value(self, v: str):
        values = re.split(r'(\r\n|\n|\r)', v)

        rs = values[1:]

        if len(rs) > 0:
            rs = [v for v in rs if v.strip()]

        return (values[0], rs)

    def _get_column_value(self, key: any, columns: dict, cur: str):
        fn = getattr(self, '_get_col_' + cur, None)

        if callable(fn):
            v = fn(columns.get(cur, ''), key, columns)
        else:
            v = columns.get(cur, '')

        return v


class HelpFormatter(BaseHelpFormatter):
    DEFAULT_COLUMNS = {
        'name': 'Parameter',
        'type': 'Type',
        'require': 'Require',
        'validation': 'Validation',
        'default': 'Default',
        'help': 'Description'
    }

    def __init__(self):
        super().__init__()

        self.columns = {**self.DEFAULT_COLUMNS}

    def enable_example(self, label: str = None):
        if label is None and 'example' not in self.columns:
            label = 'Example'

        if label is not None:
            self.set_column('example', label)

    def _get_col_require(self, v: any, key: any, columns: dict):
        return 'yes' if v else ''

    def _get_col_multiple(self, v: any, key: any, columns: dict):
        return 'yes' if v else ''

    def _get_col_type(self, v: any, key: any, columns: dict):
        r = ''

        if v == int:
            r = 'int'
        elif v == bool:
            r = 'bool'
        elif v == float:
            r = 'float'
        elif v == complex:
            r = 'complex'
        elif v == str:
            r = 'str'
        elif isinstance(v, str):
            r = v
        else:
            r = '-'

        if columns.get('list'):
            r = '{}, list'.format(r)

        return r

    def _get_col_name(self, v: any, key: any, columns: dict):
        return key

    def _get_col_default(self, v: any, key: any, columns: dict):
        return v

    def _get_col_validation(self, v: any, key: any, columns: dict):
        choices = columns.get('choices')
        validation = columns.get('validation', '')

        r = ''

        if choices:
            r = str(choices)
        elif validation:
            if isinstance(validation, str):
                r = validation
            elif isinstance(validation, (list, tuple)):
                w = len(validation)

                if w == 1:
                    r = validation[0]
                elif w >= 2:
                    r = validation[0] + ' (' + (', '.join(list(map(str, validation[1:])))) + ')'
            elif callable(validation):
                r = 'customize'

        return r

    def _get_col_help(self, v: any, key: any, columns: dict):
        if isinstance(v, (list, tuple)):
            v = v[0]

        return v

    def _get_col_example(self, v: any, key: any, columns: dict):
        help = columns.get('help', '')

        if isinstance(help, (list, tuple)) and len(help) == 2:
            r = str(help[1])
        else:
            r = ''

        return r
