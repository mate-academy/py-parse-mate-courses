from dataclasses import dataclass

import requests
from bs4 import Tag, BeautifulSoup

BASE_URL = "https://mate.academy/courses/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_course(course: Tag) -> Course:
    return Course(
        name=course.select_one("a h3").text,
        short_description=course.select_one(
            "p.typography_landingTextMain__Rc8BD.mb-32").text,
        duration=course.select("p")[-2].text
    )


def get_courses_from_page(soup: BeautifulSoup) -> list[Tag]:
    return soup.select("div.ProfessionCard_cardWrapper__2Q8_V")


def get_page(url: str) -> BeautifulSoup():
    page = requests.get(url).content
    return BeautifulSoup(page, "html.parser")


def get_all_courses() -> list[Course]:
    page = get_page(BASE_URL)
    courses = get_courses_from_page(page)
    return [get_course(course) for course in courses]
