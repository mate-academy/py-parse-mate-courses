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


def course_type(course_soup: BeautifulSoup) -> CourseType | list[CourseType]:
    if course_soup.select_one(".Button_secondary__DNIuD") is not None:
        return [CourseType.FULL_TIME, CourseType.PART_TIME]
    return CourseType.PART_TIME


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    return Course(
        name=course_soup.select_one("h3").text,
        short_description=course_soup.select(".typography_landingTextMain__Rc8BD")[1].text,
        course_type=course_type(course_soup),
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [parse_single_course(course_soup) for course_soup in courses]


all_courses = get_all_courses()

print([course.course_type for course in all_courses])
