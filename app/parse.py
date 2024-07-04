from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: Enum


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


def parse_single_course(course_soup: BeautifulSoup) -> list[Course]:
    name = course_soup.select_one(
        ".typography_landingH3__vTjok.ProfessionCard_title__Zq5ZY.mb-12"
    ).text
    short_description = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).get_text()

    full_time_button = course_soup.select_one(
        '[data-qa="fulltime-course-more-details-button"]'
    )
    part_time_button = course_soup.select_one(
        '[data-qa="fx-course-details-button"]'
    )

    courses = []

    if full_time_button:
        full_time_course = Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.FULL_TIME
        )
        courses.append(full_time_course)

    if part_time_button:
        part_time_course = Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.PART_TIME
        )
        courses.append(part_time_course)

    return courses


def get_page_content(url: str) -> BeautifulSoup:
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")


def get_all_courses() -> list[Course]:
    courses = []
    url = BASE_URL
    soup = get_page_content(url)
    course_elements = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    for course_soup in course_elements:
        courses.extend(parse_single_course(course_soup))
    return courses


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
