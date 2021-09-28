from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Dict, Any


class SpreadsheetSummaryRequest:

    def __init__(self, file_name: str, header_row: int, start_row: int, end_rows_skipped: int, columns: 'List[str]'):
        self.file_name = file_name
        self.header_row = header_row
        self.start_row = start_row
        self.end_rows_skipped = end_rows_skipped
        self.columns = columns

    @staticmethod
    def from_validated_data(validated_data: 'Dict[str, Any]'):
        return SpreadsheetSummaryRequest(
            file_name=validated_data['file_name'],
            header_row=validated_data['header_row'],
            start_row=validated_data['start_row'],
            end_rows_skipped=validated_data['end_rows_skipped'],
            columns=validated_data['columns'],
        )
