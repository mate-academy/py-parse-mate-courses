from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int
    topics_count: int


def parse_course(soup: Tag) -> Course:
    detail_url = urljoin(
        BASE_URL,
        soup.select_one("a")["href"],
    )

    detail_course = requests.get(detail_url).content
    detail_soup = BeautifulSoup(detail_course, "html.parser")
    modules_count = detail_soup.select("[class*='CourseModulesHeading_text']")[
        0
    ].text.split()[0]
    topics_count = detail_soup.select("[class*='CourseModulesHeading_text']")[
        1
    ].text.split()[0]

    return Course(
        name=soup.select_one("a > h3").text,
        short_description=soup.select_one("p:nth-child(3)").text,
        duration=soup.select_one("p > span").text,
        modules_count=int(modules_count),
        topics_count=int(topics_count),
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
