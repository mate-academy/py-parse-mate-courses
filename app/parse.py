from dataclasses import dataclass

import requests

from bs4 import BeautifulSoup, Tag


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_info_about_single_course(single_course_soup: Tag) -> Course:
    return Course(
        name=single_course_soup.select_one(
            "div.ProfessionCard_cardWrapper__JQBNJ >"
            " a.typography_landingH3__vTjok.ProfessionCard_title__Zq5ZY.mb-12"
            " > h3"
        ).text,
        short_description=single_course_soup.select_one(
            "div.ProfessionCard_cardWrapper__JQBNJ >"
            " p.typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        duration=single_course_soup.select(
            "p.typography_landingTextMain__Rc8BD"
            ".ProfessionCard_subtitle__K1Yp6.mb-24 > span"
        )[0].text
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [get_info_about_single_course(course) for course in courses]
