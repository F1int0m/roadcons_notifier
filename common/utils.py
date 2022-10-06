import datetime
import itertools
import uuid
from typing import List


def parse_args_to_link_with_name(args: List):
    if len(args) < 2:
        raise ValueError
    link = args[0]
    name = ' '.join(args[1:])
    return link, name


def get_project_id_from_url(google_sheet_url: str):
    start_substring = '/spreadsheets/d/'
    start = google_sheet_url.find(start_substring) + len(start_substring)
    end = google_sheet_url.find('/edit')

    result = google_sheet_url[start:end]
    return result


def flat_list(list_to_flat: List[List]) -> List:
    return list(itertools.chain(*list_to_flat))


def utc_now():
    return datetime.datetime.utcnow()


def uuid_str():
    return str(uuid.uuid4())


def format_alert_message(
        project: str,
        sheet: str,
        street_name: str,
        status: str
):
    return (f'Изменился статус в проекте {project}\n'
            f'на листе {sheet} \n'
            f'на улице {street_name}.\n'
            f'Новый статус: {status}')
