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
    modules: int
    topics: int
    duration: int


def fetch_html(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def parse_single_course(
        course_card: BeautifulSoup,
        course_page: BeautifulSoup,
        course_type: CourseType
) -> Course:
    return Course(
        name=course_card.select_one("a").text,
        short_description=course_card.select_one(
            "p.typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        course_type=course_type,
        modules=int(
            course_page.select_one(
                ".CourseModulesHeading_modulesNumber__UrnUh > p"
            ).text.split()[0]
        ),
        topics=int(
            course_page.select_one(
                ".CourseModulesHeading_topicsNumber__5IA8Z > p"
            ).text.split()[0]
        ),
        duration=int(
            course_page.select_one(
                ".CourseModulesHeading_courseDuration__qu2Lx > p"
            ).text.split()[0]
        ),
    )


def get_courses(
        course_type: CourseType,
        data_qa_selector: str
) -> list[Course]:
    all_courses = []

    soup = fetch_html(BASE_URL)
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    for course in courses:
        link = course.find("a", {"data-qa": data_qa_selector})
        if link:
            course_page_url = BASE_URL + link["href"]
            course_page_soup = fetch_html(course_page_url)
            course_detail_sections = course_page_soup.select(
                ".CourseModulesHeading_headingGrid__ynoxV"
            )
            for course_detail_section in course_detail_sections:
                all_courses.append(
                    parse_single_course(
                        course,
                        course_detail_section,
                        course_type
                    )
                )

    return all_courses


def get_full_time_courses() -> list[Course]:
    return get_courses(
        CourseType.FULL_TIME,
        "fulltime-course-more-details-button"
    )


def get_part_time_courses() -> list[Course]:
    return get_courses(CourseType.PART_TIME, "fx-course-details-button")


def get_all_courses() -> list[Course]:
    return get_full_time_courses() + get_part_time_courses()
