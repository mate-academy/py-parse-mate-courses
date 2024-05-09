import csv
import re
from dataclasses import dataclass, fields, astuple
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

MATE_PAGE = "https://mate.academy/"
COURDSES_OUTPUT_CSV_PATH = "courses.csv"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: int
    topics: int
    duration: int


COURSES_FIELDS = [field.name for field in fields(Course)]


def get_course(
    course: Tag,
    course_type: CourseType,
    modules_count: int,
    topics_count: int,
    duration: int,
) -> Course:

    return Course(
        name=course.select_one("a > h3").text,
        short_description=course.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        course_type=course_type,
        modules=modules_count,
        topics=topics_count,
        duration=duration,
    )


def get_full_time_link(course: Tag) -> Tag:
    full_time_link = course.select_one(
        ".ProfessionCard_buttons__a0o60 > a[data-qa^=fulltime]"
    )
    return full_time_link


def get_part_time_link(course: Tag) -> Tag:
    part_time_link = course.select_one(
        ".ProfessionCard_buttons__a0o60 > a[data-qa^=parttime]"
    )
    return part_time_link


def get_course_types(course: Tag) -> list[CourseType]:
    course_types = []
    if get_full_time_link(course):
        course_types.append(CourseType.FULL_TIME)
    if get_part_time_link(course):
        course_types.append(CourseType.PART_TIME)
    return course_types


def get_course_instance(
        course: Tag,
        course_type: CourseType,
        course_page_url: str
) -> Course:
    course_page = requests.get(course_page_url).content
    course_page_soup = BeautifulSoup(course_page, "html.parser")
    elements_wrapper = course_page_soup.select_one(
        ".CourseModulesHeading_headingGrid__ynoxV"
    )
    elements = elements_wrapper.select(
        "div > "
        "p.typography_landingTextMain__Rc8BD.CourseModulesHeading_text__bBEaP"
    )

    return get_course(
        course,
        course_type,
        *[
            int(number)
            for element in elements
            for number in re.findall(r"\d+", element.text)
        ]
    )


def get_all_courses() -> list[Course]:
    result = []
    page = requests.get(MATE_PAGE).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    for course in courses:
        for course_type in get_course_types(course):
            course_page_url = urljoin(
                MATE_PAGE,
                get_part_time_link(course).get("href")
            )
            if course_type == CourseType.FULL_TIME:
                course_page_url = urljoin(
                    MATE_PAGE,
                    get_full_time_link(course).get("href")
                )
            result.append(
                get_course_instance(course, course_type, course_page_url)
            )
    return result


def write_products_to_csv(products: [Course]) -> None:
    with open(
            COURDSES_OUTPUT_CSV_PATH,
            "w",
            encoding="utf-8",
            newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(COURSES_FIELDS)
        writer.writerows([astuple(product) for product in products])


def main() -> None:
    courses = get_all_courses()
    write_products_to_csv(courses)


if __name__ == "__main__":
    main()
