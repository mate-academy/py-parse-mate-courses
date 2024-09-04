from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    duration_and_description = course_soup.select(
        ".typography_landingTextMain__Rc8BD"
    )
    short_description = duration_and_description[1].text
    duration = duration_and_description[0].text.split("•")[0]

    return Course(
        name=name,
        short_description=short_description,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [parse_single_course(course_soup) for course_soup in courses]
