def get_project_id_from_url(google_sheet_url: str):
    start_substring = '/spreadsheets/d/'
    start = google_sheet_url.find(start_substring) + len(start_substring)
    end = google_sheet_url.find('/edit')

    result = google_sheet_url[start:end]
    return result
