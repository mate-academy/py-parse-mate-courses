import re

import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin


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


def get_single_course(
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


def get_course_types(course: Tag) -> list[CourseType]:
    course_types = []

    full_time_link = course.select_one(
        ".ProfessionCard_buttons__a0o60 > a[data-qa^=fulltime]"
    )
    part_time_link = course.select_one(
        ".ProfessionCard_buttons__a0o60 > a[data-qa^=parttime]"
    )

    if full_time_link:
        course_types.append(CourseType.FULL_TIME)
    if part_time_link:
        course_types.append(CourseType.PART_TIME)

    return course_types


def get_course_instance(
    course: Tag, course_type: CourseType, course_page_url: str
) -> Course:

    course_page_content = requests.get(course_page_url).content
    course_page_soup = BeautifulSoup(course_page_content, "html.parser")
    count_wrapper = course_page_soup.select_one(
        ".CourseModulesHeading_headingGrid__ynoxV"
    )
    count_elements = count_wrapper.select(
        "div > "
        "p.typography_landingTextMain__Rc8BD.CourseModulesHeading_text__bBEaP"
    )

    return get_single_course(
        course,
        course_type,
        *[
            int(num)
            for element in count_elements
            for num in re.findall(r"\d+", element.text)
        ]
    )


def get_all_courses() -> list[Course]:
    result = []

    base_url = "https://mate.academy"

    page = requests.get(base_url).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select("div[data-qa=profession-card]")

    for course in courses:
        for course_type in get_course_types(course):
            anchor_tag = course.select_one("a")
            course_page_url = urljoin(base_url, anchor_tag.get("href"))

            result.append(
                get_course_instance(course, course_type, course_page_url)
            )

    return result
