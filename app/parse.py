import csv
from dataclasses import dataclass, fields
from enum import Enum
from typing import List

import requests
from bs4 import BeautifulSoup, element

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


PART_TIME = "Гнучкий графік"
FULL_TIME = "Повний день"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: List[CourseType]


COURSE_TYPE_FIELD = [field.name for field in fields(Course)]


def _create_course_instance(
        name: str,
        short_description: str,
        course_type: str
) -> Course:
    if course_type == PART_TIME:
        course_type = CourseType.PART_TIME
    if course_type == FULL_TIME:
        course_type = CourseType.FULL_TIME

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type,
    )


def parse_course(course: element.Tag) -> list[Course]:
    name = course.select_one("a.ProfessionCard_title__Zq5ZY").text
    short_description = course.select(
        "p.typography_landingTextMain__Rc8BD"
    )[1].text
    course_types = [
        course.text
        for course
        in course.select("div.ProfessionCard_buttons__a0o60 > a > span")
    ]
    return [_create_course_instance(
        name=name,
        short_description=short_description,
        course_type=course_type
    ) for course_type in course_types]


def get_all_courses() -> List[Course]:
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    courses_html = soup.select("div.ProfessionCard_cardWrapper__JQBNJ")
    courses = [course for html_courses in courses_html
               for course in parse_course(html_courses)]

    return courses


def write_courses_to_csv(courses: List[Course]) -> None:
    with open("courses.csv", "w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Name", "Short Description", "Course Type"])
        for course in courses:
            csv_writer.writerow(
                [course.name, course.short_description, course.course_type]
            )


def main() -> None:
    courses = get_all_courses()
    write_courses_to_csv(courses)


if __name__ == "__main__":
    main()
