from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    duration: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: BeautifulSoup) -> list[Course]:
    if course_soup.find(attrs={
        "data-qa": "fulltime-course-more-details-button"
    }):
        types = [CourseType.FULL_TIME, CourseType.PART_TIME]
    else:
        types = [CourseType.PART_TIME]
    list_courses = []
    for element in types:
        course = Course(
            name=course_soup.select_one("h3").text.split(" ")[0],
            duration=course_soup.select(
                ".typography_landingTextMain__Rc8BD"
            )[0].text,
            short_description=course_soup.select(
                ".typography_landingTextMain__Rc8BD"
            )[1].text,
            course_type=element,
        )
        list_courses.append(course)
    return list_courses


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []
    for course in courses:
        all_courses.extend(parse_single_course(course))
    return all_courses


if __name__ == "__main__":
    all_courses = get_all_courses()
    for course in all_courses:
        print(course)
