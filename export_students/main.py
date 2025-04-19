from typing import Iterable
from uuid import UUID

import bs4
import requests

from export_students.student import Student


def export_students_from_group(group_id: UUID) -> Iterable[Student]:
    resp = requests.get(
        f"https://eu.bmstu.ru/modules/contingent3/container/{group_id}/",
        headers={
            'cookie':
                "PHPSESSID=lrn7c2kcdbc2lb2btt80ipvqi7; "
                "__portal3_login=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c3IiOnsiaWQiOjU1MzYzLCJndWlkIjoiOGIzODBiNzEtMDM"
                "0NC0xMWVkLWE0MzItMDA1MDU2YWE2NzNiIiwiYWxpYXMiOiJcdTA0MThcdTA0MjM3LTY0XHUwNDExIiwibGFzdG5hbWUiOiJcdTA0MWF"
                "cdTA0NDBcdTA0MzhcdTA0MzJcdTA0M2FcdTA0M2UiLCJmaXJzdG5hbWUiOiJcdTA0MjFcdTA0MzVcdTA0NDBcdTA0MzNcdTA0MzVcdTA"
                "0MzkiLCJtaWRkbGVuYW1lIjoiXHUwNDE1XHUwNDMyXHUwNDMzXHUwNDM1XHUwNDNkXHUwNDRjXHUwNDM1XHUwNDMyXHUwNDM4XHUwNDQ"
                "3IiwiYmlydGhkYXRlIjoiMjAwNC0wOS0yMCIsIm5hbWUiOiJcdTA0MWFcdTA0NDBcdTA0MzhcdTA0MzJcdTA0M2FcdTA0M2UgXHUwNDI"
                "xXHUwNDM1XHUwNDQwXHUwNDMzXHUwNDM1XHUwNDM5IFx1MDQxNVx1MDQzMlx1MDQzM1x1MDQzNVx1MDQzZFx1MDQ0Y1x1MDQzNVx1MDQ"
                "zMlx1MDQzOFx1MDQ0NyJ9LCJpYXQiOjE3NDUwNDE1MTAsIm5iZiI6MTc0NTA0MTUxMCwiZXhwIjoxNzQ1MDQyNzIwfQ.K2FC2eWaMNP7"
                "dLEglZzZBxkE2IaoCVmJLhkuF2qKizYj1dU7ZujYMnY15mnM3a_fGo5gCK6nSNaDPzYSWcFDQw; "
                "__portal3_info=eyJuYW1lIjoiXHUwNDFhXHUwNDQwXHUwNDM4XHUwNDMyXHUwNDNhXHUwNDNlIFx1MDQyMVx1MDQzNVx1MDQ0MFx1M"
                "DQzM1x1MDQzNVx1MDQzOSBcdTA0MTVcdTA0MzJcdTA0MzNcdTA0MzVcdTA0M2RcdTA0NGNcdTA0MzVcdTA0MzJcdTA0MzhcdTA0NDciL"
                "CJleHBpcmUiOjE3NDUwNDYzNzl9",
            'host': "eu.bmstu.ru",
            "referer": "https://eu.bmstu.ru/modules/contingent3",
        }
    )
    resp.raise_for_status()

    page = bs4.BeautifulSoup(resp.text, "html.parser")
    students_table = page.find("table", {"class": "students-table"})
    table_body = students_table.find("tbody")
    for student_elem in table_body.find_all("tr"):
        cells = list(student_elem.find_all("td"))
        yield Student(full_name=cells[1].text, id=cells[2].text, group_alias=cells[3].text)


if __name__ == "__main__":
    for student in export_students_from_group(UUID('f9833d92-8a79-11ec-b81a-0de102063aa5')):
        print(student)

