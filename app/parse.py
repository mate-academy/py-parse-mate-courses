from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    duration: int


def get_single_page() -> BeautifulSoup:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    course_soup = soup.select("div[class*=ProfessionCard_card]")
    return course_soup


def get_single_course(course_soup: BeautifulSoup) -> [Course]:
    courses = []

    name = course_soup.select_one("a[class*=ProfessionCard_title__Zq5ZY]").text
    short_description = course_soup.select_one(
        "p.typography_landingTextMain__Rc8BD.mb-32"
    ).text
    duration = int(
        course_soup.select_one("p[class*=ProfessionCard_subtitle__K1Yp6]").text[0]
    )

    part_time = course_soup.select_one("a[class*=Button_secondary__DNIuD]")
    full_time = course_soup.select_one("a[class*=Button_primary__7fH0C]")

    if part_time:
        courses.append(Course(name, short_description, CourseType.PART_TIME, duration))
    if full_time:
        courses.append(Course(name, short_description, CourseType.FULL_TIME, duration))
    return courses


def get_all_courses() -> list[Course]:
    result = []

    for course in get_single_page():
        result.extend(get_single_course(course))

    return result
