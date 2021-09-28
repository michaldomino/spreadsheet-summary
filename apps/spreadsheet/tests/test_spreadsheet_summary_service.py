import pandas
from django.test import TestCase

from apps.spreadsheet.services import SpreadsheetSummaryService
from apps.spreadsheet.tests.resources import TEST_SPREADSHEET_XLSX


class TestSpreadsheetSummaryService(TestCase):
    _SPREADSHEET_PATH = TEST_SPREADSHEET_XLSX

    def setUp(self) -> None:
        self.summary_service = SpreadsheetSummaryService(self._get_data_frame())
        super().setUp()

    def test_service_should_calculate_sum_when_correct(self):
        expected_result = {
            'ONE LINE': 31.0,
            'MULTI LINE TEXT': 546.912,
            'PERCENT': 2197.6708644
        }

        result = dict(self.summary_service.calculate_sum(['ONE LINE', 'MULTI LINE TEXT', 'PERCENT']))

        self.assertEqual(expected_result, result)

    def test_service_should_calculate_sum_when_start_row_provided(self):
        expected_result = {
            'ONE LINE': 28.0,
            'MULTI LINE TEXT': 516.912,
            'PERCENT': 2197.6608643
        }

        result = dict(self.summary_service.calculate_sum(['ONE LINE', 'MULTI LINE TEXT', 'PERCENT'], start_row=3))

        self.assertEqual(expected_result, result)

    def test_service_should_calculate_sum_when_end_rows_skipped_provided(self):
        expected_result = {
            'ONE LINE': 15.5,
            'MULTI LINE TEXT': 150.0,
            'PERCENT': 1098.8254322
        }

        result = dict(
            self.summary_service.calculate_sum(['ONE LINE', 'MULTI LINE TEXT', 'PERCENT'], end_rows_skipped=2))

        self.assertEqual(expected_result, result)
        
    def test_service_should_calculate_average_when_correct(self):
        expected_result = {
            'ONE LINE': 3.875,
            'MULTI LINE TEXT': 68.364,
            'PERCENT': 274.70885805
        }

        result = dict(self.summary_service.calculate_average(['ONE LINE', 'MULTI LINE TEXT', 'PERCENT']))

        self.assertEqual(expected_result, result)

    def test_service_should_calculate_average_when_start_row_provided(self):
        expected_result = {
            'ONE LINE': 4.666666666666667,
            'MULTI LINE TEXT': 86.152,
            'PERCENT': 366.27681071666666
        }

        result = dict(self.summary_service.calculate_average(['ONE LINE', 'MULTI LINE TEXT', 'PERCENT'], start_row=3))

        self.assertEqual(expected_result, result)

    def test_service_should_calculate_average_when_end_rows_skipped_provided(self):
        expected_result = {
            'ONE LINE': 2.5833333333333335,
            'MULTI LINE TEXT': 25.0,
            'PERCENT': 183.13757203333333
        }

        result = dict(
            self.summary_service.calculate_average(['ONE LINE', 'MULTI LINE TEXT', 'PERCENT'], end_rows_skipped=2))

        self.assertEqual(expected_result, result)

    @staticmethod
    def _get_data_frame(file_path=_SPREADSHEET_PATH, header_row=2):
        with open(file_path, 'rb') as file:
            data_frame = pandas.read_excel(file.read(), skiprows=header_row, engine='openpyxl')
            return data_frame.rename(columns=lambda column: column.strip())
