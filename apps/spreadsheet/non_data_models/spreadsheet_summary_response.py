from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from apps.spreadsheet.non_data_models import Result


class SpreadsheetSummaryResponse:

    def __init__(self, file: str, summary: 'List[Result]'):
        self.file = file
        self.summary = summary
