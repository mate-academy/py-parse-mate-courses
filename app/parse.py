from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


BASE_URL = "https://mate.academy/"


def get_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(
            ".typography_landingH3__vTjok.ProfessionCard_title__fEWio.mb-12"
            " > h3").text,
        short_description=course.select_one(
            "p.typography_landingTextMain__Rc8BD.mb-32").text,
        duration=course.select_one(
            ".typography_landingTextMain__Rc8BD"
            ".ProfessionCardTags_regularTag__dqOGj "
            "> span:last-child").text
    )


def get_page(url: str) -> BeautifulSoup:
    response = requests.get(url).content
    return BeautifulSoup(response, "html.parser")


def get_page_courses(page_soup: Tag) -> List[Course]:
    courses = page_soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    return [get_course(course) for course in courses]


def get_all_courses() -> list[Course]:
    current_page = get_page(BASE_URL)
    all_courses = get_page_courses(current_page)
    return all_courses
