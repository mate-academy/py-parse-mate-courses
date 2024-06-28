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


def parse_single_course(soup: BeautifulSoup, course_type: CourseType) -> Course:
    return Course(
        name=soup.select_one("a").text.strip(),
        short_description=soup.select_one("p.typography_landingTextMain__Rc8BD.mb-32").text.strip(),
        course_type=course_type
    )


def get_courses(course_type: CourseType, data_qa_selector: str) -> list[Course]:
    all_courses = []

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    for course in courses:
        if course.find('a', {'data-qa': data_qa_selector}):
            all_courses.append(parse_single_course(course, course_type))

    return all_courses


def get_full_time_courses() -> list[Course]:
    return get_courses(CourseType.FULL_TIME, 'fulltime-course-more-details-button')


def get_part_time_courses() -> list[Course]:
    return get_courses(CourseType.PART_TIME, 'fx-course-details-button')


def get_all_courses() -> list[Course]:
    return get_full_time_courses() + get_part_time_courses()
