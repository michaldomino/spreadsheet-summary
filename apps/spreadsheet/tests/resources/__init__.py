import os
import pathlib

_FILE_PATH = pathlib.Path(__file__)

TEST_SPREADSHEET_XLSX = os.path.join(_FILE_PATH.with_name('test_spreadsheet.xlsx'))
TEXT_FILE_TXT = os.path.join(_FILE_PATH.with_name('text_file.txt'))
