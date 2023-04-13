from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup, element

MATE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: tuple
    short_description: tuple
    course_type: CourseType


def parse_single_course(course_soup: element.Tag) -> Course:
    name = course_soup.select_one("span").text,
    short_description = course_soup.select_one("p").text,
    course_type = (
        CourseType.PART_TIME if "Вечірній" in name[0].split()
        else CourseType.FULL_TIME
    )
    return Course(
        name=name, short_description=short_description, course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]
