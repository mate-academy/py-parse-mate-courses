from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_all_courses() -> list[Course]:
    results = []
    request_courses = requests.get(BASE_URL)
    soup = BeautifulSoup(request_courses.text, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    for course in courses:
        results.append(
            Course(
                name=course.select_one("a.typography_landingH3__vTjok").text,
                short_description=course.select(
                    "p.typography_landingTextMain__Rc8BD"
                )[-1].text,
                duration=course.select(
                    ".ProfessionCard_professionTags__kCD1H >"
                    " p.typography_landingTextMain__Rc8BD"
                )[-1].text,
            )
        )

    return results


if __name__ == "__main__":
    get_all_courses()
