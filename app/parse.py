from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

import requests
from bs4 import BeautifulSoup

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def specify_course_type(course) -> List[Course]:
    full_time = course.select_one(
        ".Button_brandSecondary__DXhVs.Button_large__rIMVg.Button_button__bwept.Button_fullWidth___Ft6W")
    part_time = course.select_one(
        ".Button_brandPrimary__uJ_Nl.Button_large__rIMVg.Button_button__bwept.Button_fullWidth___Ft6W")

    if full_time and part_time:
        return parse_singe_course(course, course1=CourseType.FULL_TIME, course2=CourseType.PART_TIME)
    elif part_time:
        return parse_singe_course(course, course1=CourseType.PART_TIME)
    elif full_time:
        return parse_singe_course(course, course1=CourseType.FULL_TIME)
    return []


def parse_singe_course(soup, course1: CourseType, course2: Optional[CourseType] = None) -> List[Course]:
    courses = []

    course = Course(
        name=soup.select_one("h3").text.strip(),
        short_description=soup.select_one(".mb-32").text.strip(),
        course_type=course1,
    )
    courses.append(course)

    if course2 is not None:
        course = Course(
            name=soup.select_one("h3").text.strip(),
            short_description=soup.select_one(".mb-32").text.strip(),
            course_type=course2,
        )
        courses.append(course)

    return courses


def get_page() -> List[Course]:
    url = URL
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []
    for course in courses:
        all_courses.extend(specify_course_type(course))
    return all_courses


def get_all_courses() -> List[Course]:
    return get_page()


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
