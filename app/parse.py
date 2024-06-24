import requests

from dataclasses import dataclass
from enum import Enum
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


def parse_course(course_soup: BeautifulSoup) -> list[Course]:
    name = course_soup.select_one(
        "a[class*='ProfessionCard_title'] > h3"
    ).text
    short_description = course_soup.select_one(
        "p:not([class*='ProfessionCard_subtitle'])"
    ).text
    fulltime = course_soup.select_one(
        "a[data-qa=fulltime-course-more-details-button]"
    )
    parttime = course_soup.select_one(
        "a[data-qa=parttime-course-more-details-button]"
    )

    result = []

    if fulltime:
        result.append(Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.FULL_TIME
        ))
    if parttime:
        result.append(Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.PART_TIME
        ))

    return result


def get_all_courses() -> list[Course]:
    courses = BeautifulSoup(
        requests.get(BASE_URL).content,
        "html.parser"
    ).select("div[class*='ProfessionCard_cardWrapper']")

    result = []

    for course in courses:
        result.extend(parse_course(course))

    return result
