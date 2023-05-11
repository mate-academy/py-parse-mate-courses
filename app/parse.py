from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course_type = (
        CourseType.PART_TIME if "Вечірній" in name else CourseType.FULL_TIME
    )

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get("https://mate.academy/").content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


if __name__ == "__main__":
    print(get_all_courses())
