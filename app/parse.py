from dataclasses import dataclass
import re

import requests
from bs4 import BeautifulSoup

HOME_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: int


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    duration_text = course_soup.select_one(".mb-24").text
    duration_number = int(re.search(r"\d+", duration_text).group())
    return Course(
        name=course_soup.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=course_soup.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        duration=duration_number
    )


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [parse_single_course(course) for course in courses]


if __name__ == "__main__":
    print(get_all_courses())
