import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


all_courses = []


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_all_courses() -> list[Course]:
    global all_courses
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    for course in courses:
        name = course.select_one(
            ".typography_landingH3__vTjok."
            "ProfessionCard_title__Zq5ZY.mb-12 > h3"
        ).text
        short_description = course.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text
        course_types = course.select(
            ".ProfessionCard_buttons__a0o60 > a > span"
        )
        if len(course_types) == 2:
            all_courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.FULL_TIME
                )
            )
            all_courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.PART_TIME
                )
            )
        else:

            all_courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.PART_TIME
                )
            )
    return all_courses


get_all_courses()
