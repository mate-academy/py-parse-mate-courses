from typing import Union, List

import requests
from bs4 import BeautifulSoup

from dataclasses import dataclass
from enum import Enum

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_course_type(
        course_soup: BeautifulSoup
) -> Union[CourseType, List[CourseType], None]:
    full_time = course_soup.select_one(
        ".Button_brandSecondary__DXhVs.Button_large__rIMVg"
        ".Button_button__bwept.Button_fullWidth___Ft6W"
    )
    part_time = course_soup.select_one(
        ".Button_brandPrimary__uJ_Nl.Button_large__rIMVg"
        ".Button_button__bwept.Button_fullWidth___Ft6W"
    )

    if full_time and part_time:
        return [CourseType.FULL_TIME, CourseType.PART_TIME]
    elif full_time:
        return CourseType.FULL_TIME
    elif part_time:
        return CourseType.PART_TIME


def parse_single_course(course_soup: BeautifulSoup) -> List[Course]:
    name = course_soup.select_one(
        ".typography_landingH3__vTjok.ProfessionCard_title__Zq5ZY.mb-12"
    ).text.strip()
    short_description = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text.strip()
    course_types = parse_course_type(course_soup)

    if isinstance(course_types, list):
        courses = [
            Course(
                name=name,
                short_description=short_description,
                course_type=course_type
            )
            for course_type in course_types
        ]
    else:
        courses = [
            Course(
                name=name,
                short_description=short_description,
                course_type=course_types
            )
        ]

    return courses


def get_all_courses() -> List[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []
    for course_soup in courses:
        all_courses.extend(parse_single_course(course_soup))

    return all_courses
