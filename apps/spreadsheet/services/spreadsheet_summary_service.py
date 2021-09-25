from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from pandas import DataFrame


class SpreadsheetSummaryService:

    def __init__(self, data_frame: 'DataFrame'):
        self._data_frame = data_frame

    def calculate_sum(self, column_names: 'List[str]', start_row, end_rows_skipped):
        end_row = -end_rows_skipped if end_rows_skipped > 0 else None
        return self._data_frame[column_names][start_row:end_row].sum()

    def calculate_average(self, column_names: 'List[str]', start_row, end_rows_skipped):
        end_row = -end_rows_skipped if end_rows_skipped > 0 else None
        return self._data_frame[column_names][start_row:end_row].mean()
