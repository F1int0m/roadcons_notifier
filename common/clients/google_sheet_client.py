from logging import getLogger
from typing import List

from googleapiclient.discovery import build

import config
from common.enums import GoogleSheetEnums
from common.utils import flat_list

log = getLogger(__name__)

LISTS_TO_READ = [GoogleSheetEnums.kameralka, GoogleSheetEnums.podd, GoogleSheetEnums.avtocad]

LIST_TO_USER_COLUM = {
    GoogleSheetEnums.kameralka: 'G:G',
    GoogleSheetEnums.podd: 'G:G',
    GoogleSheetEnums.avtocad: 'Q:Q',
}

LIST_TO_STATUS_COLUMN = {
    GoogleSheetEnums.kameralka: 'H:H',
    GoogleSheetEnums.podd: 'F:F',
    GoogleSheetEnums.avtocad: 'R:R',
}
LIST_TO_STREET_NAME = {
    GoogleSheetEnums.kameralka: 'D:D',
    GoogleSheetEnums.podd: 'D:D',
    GoogleSheetEnums.avtocad: 'H:H',
}


class GoogleSheetClient:

    def __init__(self):
        service = build(
            'sheets',
            'v4',
            discoveryServiceUrl=config.DISCOVERY_URL,
            developerKey=config.API_KEY)

        self.service = service

        super().__init__()

    def get_range(self, spreadsheet_id: str, sheet_name: GoogleSheetEnums, range: str) -> List[str]:
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=f'{sheet_name}!{range}').execute()
        rows = result.get('values', [])
        return flat_list(rows)
