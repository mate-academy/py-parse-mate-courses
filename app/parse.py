from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_course(soup: Tag) -> Course:
    return Course(
        name=soup.select_one("a > h3").text,
        short_description=soup.select_one("p:nth-child(3)").text,
        duration=soup.select_one("p > span").text,
    )


def get_all_courses() -> list[Course]:
    response = requests.get(f"{BASE_URL}/").content
    courses_soup = BeautifulSoup(response, "html.parser").select(
        "[data-qa='profession-card']"
    )

    courses = []

    for course_soup in courses_soup:
        courses.append(parse_course(course_soup))

    return courses


if __name__ == "__main__":
    get_all_courses()
